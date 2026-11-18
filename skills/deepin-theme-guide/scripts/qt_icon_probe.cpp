// Read-only Qt 6 lookup probe. Built in a temporary directory when tools exist.
#include <QGuiApplication>
#include <QIcon>
#include <QPixmap>
#include <QFileInfo>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QLoggingCategory>
#include <cstdio>

static QStringList entries;
static void message(QtMsgType, const QMessageLogContext &context, const QString &text)
{
    if (QString::fromUtf8(context.category) != "qt.gui.icon.loader"
        || !text.startsWith("Resulting icon entries")) return;
    int begin = text.indexOf('('), end = text.lastIndexOf(')');
    for (QString path : text.mid(begin + 1, end - begin - 1).split(',')) {
        path = path.trimmed();
        if (QFileInfo::exists(path)) entries.append(QFileInfo(path).canonicalFilePath());
    }
}

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    QByteArray data;
    char buffer[4096];
    while (size_t count = std::fread(buffer, 1, sizeof(buffer), stdin)) data.append(buffer, count);
    auto request = QJsonDocument::fromJson(data).object();
    auto oldTheme = QIcon::themeName();
    if (!request["staged_parent"].toString().isEmpty()) {
        auto paths = QIcon::themeSearchPaths();
        paths.prepend(request["staged_parent"].toString());
        QIcon::setThemeSearchPaths(paths);
    }
    QIcon::setThemeName(request["theme"].toString());
    qInstallMessageHandler(message);
    QLoggingCategory::setFilterRules("qt.gui.icon.loader.debug=true");
    QJsonArray rows;
    for (const auto &value : request["names"].toArray()) {
        entries.clear();
        const QString name = value.toString();
        QIcon icon = QIcon::fromTheme(name);
        for (const auto &sizeValue : request["sizes"].toArray()) {
            const int size = sizeValue.toInt();
            auto pixmap = icon.pixmap(size, size);
            QJsonObject row;
            row["name"] = name;
            row["size"] = size;
            row["rendered"] = !pixmap.isNull();
            row["files"] = QJsonArray::fromStringList(entries);
            rows.append(row);
        }
    }
    QJsonObject out;
    out["available"] = true;
    out["resolver"] = "qt6";
    out["default_theme"] = oldTheme;
    out["search_paths"] = QJsonArray::fromStringList(QIcon::themeSearchPaths());
    out["rows"] = rows;
    std::puts(QJsonDocument(out).toJson(QJsonDocument::Compact).constData());
}
