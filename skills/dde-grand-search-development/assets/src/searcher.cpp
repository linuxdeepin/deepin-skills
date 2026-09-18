// SPDX-FileCopyrightText: 2026 UnionTech Software Technology Co., Ltd.
//
// SPDX-License-Identifier: GPL-3.0-or-later

#include "searcher.h"

#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QJsonParseError>
#include <QCoreApplication>
#include <QLoggingCategory>

Q_LOGGING_CATEGORY(logMyPlugin, "myplugin.search")

// ── 协议常量（与 daemon 源码 utils/searchpluginprotocol.h 对应）──────
static const char *const PROTOCOL_VERSION = "1.0";
static const char *const PROTOCOL_MISSIONID = "mID";
static const char *const PROTOCOL_CONTENT = "cont";
static const char *const PROTOCOL_GROUP = "group";
static const char *const PROTOCOL_ITEMS = "items";
static const char *const PROTOCOL_ITEM = "item";
static const char *const PROTOCOL_NAME = "name";
static const char *const PROTOCOL_ICON = "icon";
static const char *const PROTOCOL_TYPE = "type";
static const char *const PROTOCOL_ACTION = "action";
static const char *const ACTION_OPEN = "openitem";

// 结果项使用的图标与 MIME type，按业务修改
static const char *const RESULT_ICON = "system-search";
static const char *const RESULT_TYPE = "application/x-mysearch-result";

MySearcher::MySearcher(QObject *parent)
    : QObject(parent)
{
    qCInfo(logMyPlugin) << "My search plugin initialized";
}

MySearcher::~MySearcher()
{
}

// ═══════════════════════════════════════════════════════════════════
// Search：解析输入 → 执行搜索 → 构造结果 JSON
// 必须可被 Stop 中断，且整体耗时不能超过 daemon 的 25 秒超时
// ═══════════════════════════════════════════════════════════════════
QString MySearcher::search(const QString &json)
{
    SearchInput input = parseSearchInput(json);

    // mID 为空时 daemon 侧也会丢弃结果，这里直接返回空
    if (input.mID.isEmpty()) {
        qCWarning(logMyPlugin) << "Invalid search input: missing mID";
        return buildEmptyResult(input.mID);
    }

    // 版本必须为 1.0，否则不处理
    if (input.ver != PROTOCOL_VERSION) {
        qCWarning(logMyPlugin) << "Unsupported protocol version:" << input.ver;
        return buildEmptyResult(input.mID);
    }

    qCDebug(logMyPlugin) << "Search - mID:" << input.mID << "keyword:" << input.cont;

    if (input.cont.isEmpty())
        return buildEmptyResult(input.mID);

    // 中断标志需在每次搜索开始前清理
    clearInterrupt(input.mID);

    QList<QPair<QString, QString>> items = doSearch(input.cont);

    // 搜索过程中被 Stop 中断：返回已得到的部分结果或空结果
    if (isInterrupted(input.mID)) {
        qCDebug(logMyPlugin) << "Search interrupted - mID:" << input.mID;
        clearInterrupt(input.mID);
        return buildEmptyResult(input.mID);
    }

    clearInterrupt(input.mID);

    if (items.isEmpty())
        return buildEmptyResult(input.mID);

    return buildResult(input.mID, items);
}

// ═══════════════════════════════════════════════════════════════════
// Stop：标记任务中断，使正在执行的 Search 尽快返回
// ═══════════════════════════════════════════════════════════════════
bool MySearcher::stop(const QString &json)
{
    QJsonParseError error;
    QJsonDocument doc = QJsonDocument::fromJson(json.toUtf8(), &error);
    if (error.error != QJsonParseError::NoError) {
        qCWarning(logMyPlugin) << "Stop: JSON parse error:" << error.errorString();
        return false;
    }

    const QString mID = doc.object().value(PROTOCOL_MISSIONID).toString();
    if (mID.isEmpty())
        return false;

    {
        QMutexLocker locker(&m_mutex);
        m_interruptedIDs.insert(mID);
    }

    qCDebug(logMyPlugin) << "Stop search task:" << mID;
    return true;
}

// ═══════════════════════════════════════════════════════════════════
// Action：对结果项执行操作（当前仅 openitem）
// ═══════════════════════════════════════════════════════════════════
bool MySearcher::action(const QString &json)
{
    QJsonParseError error;
    QJsonDocument doc = QJsonDocument::fromJson(json.toUtf8(), &error);
    if (error.error != QJsonParseError::NoError) {
        qCWarning(logMyPlugin) << "Action: JSON parse error:" << error.errorString();
        return false;
    }

    const QJsonObject root = doc.object();
    const QString ver = root.value("ver").toString();
    const QString act = root.value(PROTOCOL_ACTION).toString();
    const QString item = root.value(PROTOCOL_ITEM).toString();

    if (ver != PROTOCOL_VERSION || item.isEmpty()) {
        qCWarning(logMyPlugin) << "Invalid action input";
        return false;
    }

    qCDebug(logMyPlugin) << "Action:" << act << "item:" << item;

    // Action 由 daemon 新建的临时连接发起，不要依赖搜索期间的内存状态。
    // 这里把定位信息编码在 item 中（自描述），因此无需缓存即可处理。
    if (act == ACTION_OPEN)
        return doOpenItem(item);

    qCWarning(logMyPlugin) << "Unsupported action:" << act;
    return false;
}

// ── 协议解析 ────────────────────────────────────────────────────────

MySearcher::SearchInput MySearcher::parseSearchInput(const QString &json) const
{
    SearchInput input;

    QJsonParseError error;
    QJsonDocument doc = QJsonDocument::fromJson(json.toUtf8(), &error);
    if (error.error != QJsonParseError::NoError) {
        qCWarning(logMyPlugin) << "JSON parse error:" << error.errorString();
        return input;
    }

    const QJsonObject root = doc.object();
    input.ver = root.value("ver").toString();
    input.mID = root.value(PROTOCOL_MISSIONID).toString();
    input.cont = root.value(PROTOCOL_CONTENT).toString().trimmed();
    return input;
}

// ── 结果构造 ────────────────────────────────────────────────────────

QString MySearcher::buildResult(const QString &mID,
                                const QList<QPair<QString, QString>> &items) const
{
    QJsonObject root;
    // 结果 JSON 的 ver 必须回填 1.0，否则 daemon 丢弃整个结果集
    root["ver"] = PROTOCOL_VERSION;
    root[PROTOCOL_MISSIONID] = mID;

    QJsonObject group;
    // 分组名由插件负责本地化，框架只做透传
    group[PROTOCOL_GROUP] = QCoreApplication::translate("MySearcher", "My Search");

    QJsonArray itemArray;
    for (const auto &pair : items) {
        QJsonObject item;
        // item / name / type 三个字段必须非空，否则该结果项被 daemon 跳过
        item[PROTOCOL_ITEM] = pair.first;
        item[PROTOCOL_NAME] = pair.second;
        item[PROTOCOL_ICON] = QString::fromLatin1(RESULT_ICON);
        item[PROTOCOL_TYPE] = QString::fromLatin1(RESULT_TYPE);
        itemArray.append(item);
    }

    group[PROTOCOL_ITEMS] = itemArray;

    QJsonArray contents;
    contents.append(group);
    root[PROTOCOL_CONTENT] = contents;

    return QString::fromUtf8(QJsonDocument(root).toJson(QJsonDocument::Compact));
}

QString MySearcher::buildEmptyResult(const QString &mID) const
{
    QJsonObject root;
    root["ver"] = PROTOCOL_VERSION;
    root[PROTOCOL_MISSIONID] = mID;
    // 无结果时返回空数组，不要省略 cont 字段
    root[PROTOCOL_CONTENT] = QJsonArray();

    return QString::fromUtf8(QJsonDocument(root).toJson(QJsonDocument::Compact));
}

// ── 中断管理 ────────────────────────────────────────────────────────

bool MySearcher::isInterrupted(const QString &mID) const
{
    QMutexLocker locker(&m_mutex);
    return m_interruptedIDs.contains(mID);
}

void MySearcher::clearInterrupt(const QString &mID)
{
    QMutexLocker locker(&m_mutex);
    m_interruptedIDs.remove(mID);
}

// ═══════════════════════════════════════════════════════════════════
// 业务逻辑（按需替换）
// ═══════════════════════════════════════════════════════════════════

QList<QPair<QString, QString>> MySearcher::doSearch(const QString &keyword) const
{
    QList<QPair<QString, QString>> results;

    // 示例：简单的前缀匹配。实际实现中应：
    //   1. 先用规则快速排除不可能匹配的输入
    //   2. 搜索循环中周期检查中断标志，避免超过 25 秒超时
    //   3. 只返回最相关的少量结果（跨组累计上限 100 项）
    //
    // 中断检查示例（在长循环中调用）：
    //   if (isInterrupted(mID)) return results;

    const QString lowered = keyword.toLower();
    const QStringList candidates { QStringLiteral("example-alpha"),
                                   QStringLiteral("example-beta") };

    for (const QString &candidate : candidates) {
        if (candidate.contains(lowered)) {
            // item 采用自描述格式，便于 Action 阶段定位
            results.append({ QStringLiteral("mysearch:") + candidate, candidate });
        }
    }

    return results;
}

bool MySearcher::doOpenItem(const QString &item)
{
    // 示例：解析自描述 item 并执行操作
    static const QString prefix = QStringLiteral("mysearch:");
    if (!item.startsWith(prefix))
        return false;

    const QString target = item.mid(prefix.size());
    qCInfo(logMyPlugin) << "Open item:" << target;

    // 实际实现：打开文件、跳转应用、复制内容等
    return true;
}
