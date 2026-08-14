# DConfig C++ 使用

## 1. 直接使用 DConfig

### 1.1 头文件与 CMake

```cpp
#include <DConfig>

// CMake（详见 [app-dev-with-dtk.md](../app-dev-with-dtk.md)）
// v20/v25 DTK5: find_package(DtkCore) + Dtk::Core
// v25 DTK6: find_package(Dtk6Core) + Dtk6::Core
```

### 1.2 基本用法

使用入口阶段已经固定的 `configId` 创建对象；默认 appId 由
`DSGApplication::id()` 获取，工程也可以通过 `DSG_APP_ID` 声明 appId。

```cpp
const QString configId = QStringLiteral("org.deepin.example.settings");
auto *config = new DConfig(configId, QString(), this);
if (!config->isValid()) {
    qWarning() << "DConfig is unavailable; using application defaults";
    // 保留默认值，应用仍应能够启动。
}

// 读取
bool canExit = config->isValid()
             ? config->value("canExit", true).toBool()
             : true;

if (config->isValid()) {
    // 写入
    config->setValue("canExit", false);

    // 监听变化
    connect(config, &DConfig::valueChanged, [](const QString &key) {
        qInfo() << "Config changed:" << key;
    });
}

if (config->isValid()) {
    // 重置为默认值
    config->reset("canExit");

    // 查询是否为默认值
    config->isDefaultValue("canExit");
}
```

### 1.3 创建方式

```cpp
// 默认：使用 DSGApplication::id() 获取 appId；工程可通过 DSG_APP_ID 声明
explicit DConfig(const QString &name, const QString &subpath = QString(),
                 QObject *parent = nullptr);

// 仅在无法使用默认 appId 时显式指定
static DConfig *create(const QString &appId, const QString &name,
                       const QString &subpath = QString(),
                       QObject *parent = nullptr);

// 应用无关配置
static DConfig *createGeneric(const QString &name,
                              const QString &subpath = QString(),
                              QObject *parent = nullptr);

// 全局设置
static void setAppId(const QString &appId);
static QThread *globalThread();
```

> **注意**：默认 appId 无法满足需求时，才使用 `create()` 传入入口阶段固定的
> `appId` 和 `configId`。

应用不应自行拼接配置目录或使用 `QSettings` 替代 DConfig 的持久化职责。配置元数据不可用时使用代码中的 fallback，并通过日志记录一次原因；不要因为配置服务不可用而阻塞主窗口创建。

### 1.4 实例方法

```cpp
// 读写
QVariant value(const QString &key, const QVariant &fallback = QVariant()) const;
void setValue(const QString &key, const QVariant &value);

// 查询
QStringList keyList() const;
bool isValid() const;
bool isDefaultValue(const QString &key) const;
bool isReadOnly(const QString &key) const;

// 属性
QString name() const;
QString subpath() const;

// 重置
void reset(const QString &key);
```

### 1.5 信号

```cpp
Q_SIGNALS:
    void valueChanged(const QString &key);
```

### 1.6 带 subpath 使用

```cpp
// subpath 用于配置分层，格式以 / 开头
auto *configV1 = new DConfig("org.deepin.example.settings", QString(), this);
auto *configV2 = new DConfig("org.deepin.example.settings", "/v2", this);
```

## 2. dconfig2cpp：JSON 生成类型安全的 C++ 类

### 2.1 工具用法

```bash
dconfig2cpp -c ExampleConfig \
    -o example_config.hpp \
    configs/org.deepin.example.settings.json
```

选项：

| 选项 | 说明 |
|------|------|
| `-c` / `--class-name` | 生成类名（默认 `dconfig_` + 文件名） |
| `-o` / `--output` | 输出头文件路径 |
| `--force-request-thread` | 强制传入 QThread 参数 |
| `--no-comment` | 不生成注释 |

### 2.2 生成类特性

- 每个配置项对应一个 `Q_PROPERTY`，类型自动推导：`bool` / `qlonglong` / `double` / `QString` / `QList<QVariant>` / `QVariantMap`
- `create(appId, subpath, parent)` / `createGeneric(subpath, parent)` 等工厂方法
- 线程安全的异步初始化（`DConfig::globalThread()`）
- `valueChanged(key, value)` 和各属性 `xxxChanged()` 信号
- `isInitializeSucceeded()` / `isInitializeFailed()` / `isInitializing()` 状态查询

### 2.3 使用生成类

```cpp
#include "example_config.hpp"

class MyWindow : public QWidget {
    ExampleConfig *m_cfg;
    void initConfig() {
        // 参数是 appId；配置 ID 已由生成类对应的 meta 文件确定。
        m_cfg = ExampleConfig::create("org.deepin.example");

        // 连接初始化信号，receiver 为 m_cfg 自身
        connect(m_cfg, &ExampleConfig::configInitializeSucceed, m_cfg, [this]() {
            qInfo() << "Config ready, canExit:" << m_cfg->canExit();
        });
        connect(m_cfg, &ExampleConfig::configInitializeFailed, m_cfg, [this]() {
            qWarning() << "Config init failed";
        });

        // 监听属性变化
        connect(m_cfg, &ExampleConfig::canExitChanged, m_cfg, [this]() {
            qInfo() << "canExit changed:" << m_cfg->canExit();
        });
        connect(m_cfg, &ExampleConfig::valueChanged, m_cfg,
                [this](const QString &key, const QVariant &value) {
            qInfo() << key << "->" << value;
        });
    }

    void saveConfig() {
        if (!m_cfg->isInitializeSucceeded())
            return;

        // 类型安全读写
        m_cfg->setCanExit(false);

        // 重置
        m_cfg->resetCanExit();

        // 获取底层 DConfig 对象
        auto *dconfig = m_cfg->config();
    }
};
```

> **注意**：`configInitializeSucceed` 信号回调中使用 `m_cfg` 而非信号参数中的 `DConfig*` 指针。信号确保回调执行时配置已完全初始化，直接通过生成的属性读写即可。

### 2.4 CMake 集成

```cmake
find_package(Dtk6Core REQUIRED)

dtk_add_config_to_cpp(GENERATED_SOURCES
    ${CMAKE_SOURCE_DIR}/configs/org.deepin.example.settings.json
    CLASS_NAME ExampleConfig
    OUTPUT_FILE_NAME example_config.hpp)
```

### 2.5 生成类状态机

```
Invalid → Initializing → Succeeded  (初始化成功)
                       → Failed     (初始化失败)
                       → Destroyed  (对象销毁)
```

- 初始化中可安全销毁对象
- 初始化完成前读取属性返回 meta 中定义的默认值
- 初始化后 `config()` 方法返回底层 `DConfig` 对象

## 3. 相关文档

- [concepts.md](concepts.md) - 核心概念
- [dconfig-dbus.md](dconfig-dbus.md) - DBus 方式
- [dconfig-debug.md](dconfig-debug.md) - 调试
