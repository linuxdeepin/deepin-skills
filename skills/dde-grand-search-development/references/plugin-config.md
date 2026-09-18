# 插件配置与运行模式

扩展搜索插件通过 **INI 格式的 `.conf` 文件**接入。daemon 启动时扫描插件目录，解析配置并据此发现、激活、管理插件。

## 1. 接入方式

| 项 | 要求 |
|----|------|
| 格式 | INI（`QSettings::IniFormat` 解析） |
| 后缀 | 必须为 `.conf` |
| 存放路径 | `/usr/lib/$PLATFORM/dde-grand-search-daemon/plugins/searcher/` |
| `$PLATFORM` | 平台架构目录，x86_64 下为 `x86_64-linux-gnu` |
| 完整示例 | `/usr/lib/x86_64-linux-gnu/dde-grand-search-daemon/plugins/searcher/myplugin.conf` |
| 生效方式 | **重启 `dde-grand-search-daemon`** |

路径不要硬编码：在 CMake 中用 `${CMAKE_INSTALL_FULL_LIBDIR}/dde-grand-search-daemon/plugins/searcher` 表达，`CMAKE_INSTALL_FULL_LIBDIR` 会自动展开为 `/usr/lib/<arch>`。

> INI 解析注意事项：`;` 在 INI 中是注释起始符，字段值中不要出现分号；字段名大小写敏感（`Mode` 的值大小写不敏感，`Name`/`DBusService` 等键名必须严格按表书写）。

## 2. 配置字段

根节点固定为 `[Grand Search]`，缺省会导致整个配置文件被忽略。

| 字段 | 名称 | 必须 | 说明 |
|------|------|------|------|
| `Name` | 插件名称 | 是 | 插件唯一 ID，需全局唯一。推荐 `com.company.app.xxx` 格式。**同时是结果项 `searcher` 字段的值，也是 `OpenWithPlugin` 路由插件的依据** |
| `Mode` | 运行模式 | 否 | `Auto` / `Manual` / `Trigger`，默认 `Manual` |
| `Priority` | 优先级 | 仅 Auto | `0`/`1`/`2`，非法值回退为 `2`（Low） |
| `InterfaceVersion` | 协议版本 | 是 | 当前仅 `1.0`；不受支持时该插件被跳过 |
| `DBusService` | 服务名 | 是 | 插件注册的 DBus 服务名 |
| `DBusAddress` | 服务地址 | 是 | 插件注册的 DBus 对象路径 |
| `DBusInterface` | 服务接口 | 是 | 插件注册的 DBus 接口名 |
| `Exec` | 可执行程序路径 | 仅 Auto | 启动插件进程的命令，支持带参数 |

字段校验失败（缺必填项）时，daemon 只打印一条 warning 并跳过该插件，不会有任何界面提示。

### 配置模板

模板见 [assets/conf/plugin.conf.in](../assets/conf/plugin.conf.in)：

```ini
[Grand Search]
Name=com.example.MySearch
Mode=Auto
Priority=1
DBusService=com.example.MySearch
DBusAddress=/com/example/MySearch
DBusInterface=com.example.MySearch.SearchPlugin
InterfaceVersion=1.0
Exec=@PLUGIN_EXEC_PATH@
```

其中 `@PLUGIN_EXEC_PATH@` 由 CMake `configure_file` 注入，指向插件可执行文件的最终安装路径，避免手写架构相关路径。

## 3. 运行模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `Auto` | 由 daemon 启动并控制运行时间。daemon 根据 `Priority` 决定启动时机，并按优先级守护进程 | 独立的搜索服务进程，由 daemon 统一管理生命周期 |
| `Manual` | 由用户或其他方式控制搜索服务启动，daemon 只调用其 DBus 接口 | 插件由其他系统服务管理，或插件本身就是某个应用的一部分 |
| `Trigger` | 由 DBus 自启动机制控制。daemon 直接访问插件的 DBus 服务，未启动时由 DBus 依据 `.service` 文件自动拉起 | 需要按需启动、不希望常驻后台的插件 |

> `Trigger` 模式从 5.1.1 版本开始支持。使用前确认目标系统的 `dde-grand-search` 版本。

### 3.1 模式选择建议

| 需求 | 推荐模式 |
|------|----------|
| 独立的小工具进程，随搜索按需使用，不希望常驻 | `Trigger`（需安装 `.service` 文件） |
| 需要预热索引、首次搜索要快 | `Auto` + `Priority=0`（daemon 启动时常驻） |
| 搜索时才需要，但希望避免每次启动开销 | `Auto` + `Priority=1`（首次搜索时启动并常驻） |
| 搜索开销小、空闲可退出 | `Auto` + `Priority=2`（不守护，空闲退出） |
| 搜索能力是某个已运行应用的一部分 | `Manual` |

### 3.2 Trigger 模式补充要求

`Trigger` 模式还需要在 `/usr/share/dbus-1/services/` 下安装 `.service` 文件，声明 DBus 服务名与可执行文件的映射：

```ini
[D-BUS Service]
Name=com.example.MySearch
Exec=/usr/lib/x86_64-linux-gnu/dde-grand-search-daemon/plugins/searcher/myplugin
```

daemon 激活 `Trigger` 插件时向 `org.freedesktop.DBus.Peer.Ping` 发消息（5 秒超时），由 DBus 依据该文件拉起进程。

## 4. 优先级与进程守护

`Priority` 仅在 `Auto` 模式下有效：

| 优先级 | 值 | 启动时机 | 守护机制 |
|--------|-----|----------|----------|
| `High` | 0 | daemon 启动时常驻启动 | 守护运行，异常退出后自动重启（最多 3 次） |
| `Middle` | 1 | 用户发起搜索时启动 | 守护运行，异常退出后自动重启（最多 3 次） |
| `Low` | 2 | 用户发起搜索时启动 | 不守护，空闲后退出，异常退出后不自动重启 |

`Auto` 模式的进程管理行为（源码 `PluginProcess`）：

1. **启动**：daemon 通过 `QProcess` 启动 `Exec` 指定的程序；
2. **命令解析**：`Exec` 按空格拆分出可执行程序与参数，因此**路径中不能含空格**；
3. **守护**：`Priority <= Middle` 的插件加入守护列表，进程进入 `NotRunning` 状态时自动重启；
4. **重启限制**：最多重启 3 次，之后放弃（日志 `Too many failures`）；
5. **稳定性检查**：进程启动后 1 分钟检查一次，仍在运行则清除重启计数；
6. **退出**：daemon 退出时先 `terminate()` 并等待 1 秒，超时则 `kill()`。

`Exec` 示例（带参数）：

```ini
Exec=/usr/lib/x86_64-linux-gnu/dde-grand-search-daemon/plugins/searcher/myplugin --config /etc/myplugin.conf
```

## 5. 内置搜索项冲突

以下名称已被内置搜索器占用，插件的 `Name` **不能与之相同**，否则该 `.conf` 被直接忽略：

| 内置搜索项名称 | 说明 |
|----------------|------|
| `com.deepin.dde-grand-search.file-deepin` | 文件搜索 |
| `com.deepin.dde-grand-search.app-desktop` | 应用搜索 |
| `com.deepin.dde-grand-search.dde-control-center-setting` | 控制中心设置搜索 |
| `com.deepin.dde-grand-search.web-statictext` | Web 静态文本搜索 |
| `com.deepin.dde-grand-search.semantic` | 语义搜索 |
| `com.deepin.dde-grand-search.ocr-text` | OCR 文本搜索 |
| `com.deepin.dde-grand-search.file-fulltext` | 文件全文搜索 |

另外，同一目录下 `Name` 重复的 `.conf` 只会保留第一个（按文件名排序），后续的被忽略。多个插件目录时同理。

## 6. 三个示例配置

**Auto 模式（daemon 管理进程）**

```ini
[Grand Search]
Name=com.example.CalculatorSearch
Mode=Auto
Priority=1
DBusService=com.example.CalculatorSearch
DBusAddress=/com/example/CalculatorSearch
DBusInterface=com.example.CalculatorSearch.SearchPlugin
InterfaceVersion=1.0
Exec=/usr/lib/x86_64-linux-gnu/dde-grand-search-daemon/plugins/searcher/calculator-search
```

**Manual 模式（外部控制启动）**

```ini
[Grand Search]
Name=com.example.CalculatorSearch
Mode=Manual
DBusService=com.example.CalculatorSearch
DBusAddress=/com/example/CalculatorSearch
DBusInterface=com.example.CalculatorSearch.SearchPlugin
InterfaceVersion=1.0
```

**Trigger 模式（DBus 自启动）**

```ini
[Grand Search]
Name=com.example.CalculatorSearch
Mode=Trigger
DBusService=com.example.CalculatorSearch
DBusAddress=/com/example/CalculatorSearch
DBusInterface=com.example.CalculatorSearch.SearchPlugin
InterfaceVersion=1.0
```

## 7. 配置与实现的对应关系

配置中的 DBus 三要素必须与插件代码中的注册调用逐字符一致：

| `.conf` 字段 | 插件代码对应 |
|--------------|--------------|
| `DBusService` | `QDBusConnection::sessionBus().registerService(DBus_SERVICE_NAME)` |
| `DBusAddress` | `QDBusConnection::sessionBus().registerObject(DBUS_OBJECT_PATH, &searcher)` |
| `DBusInterface` | Adaptor 的 `Q_CLASSINFO("D-Bus Interface", "...")` |

任何一处不一致的表现都是：插件进程正常运行、日志无异常，但全局搜索永远没有该插件的结果，daemon 日志中出现 `no such method` 或调用错误。

## 8. 配置文件常量

daemon 源码 `utils/searchpluginconf.h` 中的常量定义，可用于交叉核对字段名：

```cpp
#define PLUGININTERFACE_CONF_ROOT             "Grand Search"
#define PLUGININTERFACE_CONF_NAME             "Name"
#define PLUGININTERFACE_CONF_MODE             "Mode"
#define PLUGININTERFACE_CONF_MODE_AUTO        "auto"
#define PLUGININTERFACE_CONF_MODE_MANUAL      "manual"
#define PLUGININTERFACE_CONF_MODE_TRIGGER     "trigger"
#define PLUGININTERFACE_CONF_PRIORITY         "Priority"
#define PLUGININTERFACE_CONF_DBUSSERVICE      "DBusService"
#define PLUGININTERFACE_CONF_DBUSADDRESS      "DBusAddress"
#define PLUGININTERFACE_CONF_DBUSINTERFACE    "DBusInterface"
#define PLUGININTERFACE_CONF_INTERFACEVERSION "InterfaceVersion"
#define PLUGININTERFACE_CONF_EXEC             "Exec"
```

> 注意：`Mode` 的三个值在源码中是小写常量，但 `PluginLoader::readInfo` 会先 `toLower()` 再比较，因此配置中写 `Auto`/`auto`/`AUTO` 均可。
