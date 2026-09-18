# 常见陷阱与反模式

本文件汇总开发全局搜索扩展插件时最容易踩的坑。这些问题大多**不会报错**，只表现为「插件没反应」或「结果不出现」，排查成本很高。

## 1. 接口与注册

- **把插件做成 `.so` 动态库**：全局搜索扩展插件是 **DBus 服务进程**，不需要 IID、`Q_PLUGIN_METADATA`、`QPluginLoader`。做成 `.so` 会被 daemon 完全忽略。
- **注册到系统总线**：必须用 `QDBusConnection::sessionBus()`。注册到 system bus 后 daemon 在会话总线上找不到服务。
- **Adaptor 不是导出对象的子对象**：`SearchPluginAdaptor adaptor(&searcher)` 的父对象必须是 `searcher`，否则对象导出后不带 Adaptor 接口，DBus 上找不到 `Search` 方法。
- **接口名与 `.conf` 不一致**：`Q_CLASSINFO("D-Bus Interface", ...)` 必须与 `DBusInterface` 逐字符一致。不一致时 daemon 调用报错，插件本身运行正常，极易误判为「daemon 没调用我」。
- **对象路径与 `.conf` 不一致**：`registerObject` 的路径必须与 `DBusAddress` 一致。
- **方法名大小写错误**：必须是 `Search`/`Stop`/`Action`。`search`/`stop` 这样的小写方法名在 DBus 上不匹配。
- **方法签名错误**：必须是 `Search(s)→s`、`Stop(s)→b`、`Action(s)→b`。用 `Introspect` 核对。
- **用 `qdbusxml2cpp -p` 生成 Interface 而非 `-a` 生成 Adaptor**：插件侧需要 Adaptor。

## 2. 版本一致性

- **结果 JSON 的 `ver` 没回填或填错**：`ConvertorV1_0::result` 会校验 `ver == "1.0"`，不匹配时**整个结果集被丢弃**，日志只有一条 `Invalid result format from plugin`。这是最常见也最难发现的坑之一。
- **三处版本不一致**：`.conf` 的 `InterfaceVersion`、接口实现、JSON `ver` 必须都是 `1.0`。
- **自行发明版本号**（如 `"1.1"`、`"2.0"`）：daemon 不支持，插件会被跳过。

## 3. 结果 JSON

- **`item`/`name`/`type` 任一为空**：该结果项被静默跳过，不会报错。
- **`group` 为空**：整个分组被跳过。
- **`cont` 不是数组**：例如返回 `{}` 或 `null`，解析结果为空。
- **`cont` 字段缺失**：解析为空结果（合法但无内容）。无结果时应返回 `"cont": []`。
- **`mID` 未回填或与输入不一致**：`mID` 为空时整个结果被丢弃。
- **超过 100 项**：跨所有分组累计，超出部分被静默丢弃。不要指望「返回全部再让界面分页」。
- **想用扩展属性做排序或拖尾**：`itemLevel`/`itemTailer`/`itemWeight` 等**只对内置搜索器生效**，第三方插件的 `extra` 不会被填充。需要展示附加信息就写进 `name` 文本。
- **用 `type` 做展示**：`type` 不展示，它用于匹配预览插件，应填 MIME type。

## 4. 国际化

- **依赖框架翻译 `group` 和 `name`**：daemon 与前端只做透传。内置分组名有翻译映射表，**自定义分组名原样显示**。插件必须自己返回本地化文本。
- **只提供中文文案**：系统语言非中文时界面会显示中文，应使用 Qt 翻译机制（`tr()` + `.ts`/`.qm`）。

## 5. 中断与超时

- **`Search` 不可中断**：`Stop` 被调用后 `Search` 仍继续执行，界面会卡在搜索态直到 25 秒超时。
- **在 `Search` 里同步阻塞等待**：会占住事件循环，导致 DBus 无法响应 `Stop`，也无法处理新请求。
- **长时间独占锁**：`Search` 与 `Action` 可能来自不同线程，缓存需要加锁，但不要在持锁期间做耗时计算。
- **忽略「单次搜索互斥」**：上一次搜索未结束时 daemon 会跳过新搜索（`Search already in progress`），表现为「快速输入时结果不更新」。

## 6. 配置与部署

- **改 `.conf` 后不重启 daemon**：配置只在 daemon 启动时读取一次，改完必须重启。
- **`Exec` 路径含空格**：`Exec` 按空格拆分命令，路径含空格会被拆错。
- **`Auto` 模式不填 `Exec`**：`readInfo` 会因缺少 `Exec` 而跳过该插件。
- **`Manual`/`Trigger` 模式填 `Exec`**：字段会被忽略，不要指望它能启动进程。
- **`Trigger` 模式不安装 `.service` 文件**：DBus 无法自动拉起，服务永远不可用。
- **`Name` 与内置搜索项冲突**：该 `.conf` 被直接忽略。
- **`Name` 与其他插件重复**：只保留按文件名排序的第一个。
- **INI 值里出现分号**：`;` 是 INI 注释符，会把后面的内容截断。
- **INI 根节点写错**：必须是 `[Grand Search]`，否则整个配置被忽略。
- **硬编码安装路径**：应使用 `${CMAKE_INSTALL_FULL_LIBDIR}/dde-grand-search-daemon/plugins/searcher`，让 CMake 展开架构目录。
- **可执行文件安装到 `bin/`**：插件可执行文件应与 `.conf` 一起放在 searcher 插件目录下，`Exec` 指向该位置。

## 7. Action 与状态

- **`Action` 依赖搜索期间的内存缓存**：`Action` 走的是新建的临时 `PluginLiaison`，进程可能已退出。优先把定位信息编码进 `item` 字段（自描述），不要依赖易失状态。
- **`item` 不唯一或不可解析**：`item` 必须组内唯一，且能让插件在 `Action` 时定位到具体结果。
- **依赖 `Action` 的返回值**：daemon 不处理 `Action` 的返回值，但插件仍应返回 `true`/`false` 便于排查。
- **期待 daemon 传其他 `action` 值**：daemon 只会传 `openitem`，其他操作类型需由插件自行扩展且不会被触发。

## 8. 不要做的事

- 不要把搜索插件实现为 `.so`、声明 IID 或使用 `Q_PLUGIN_METADATA`
- 不要在系统总线上注册服务
- 不要在结果 JSON 中省略 `ver` 或填写非 `1.0` 的值
- 不要返回超过 100 项结果并期待全部展示
- 不要把 `itemLevel`、`itemTailer` 等扩展属性当作第三方插件可用能力
- 不要依赖框架自动翻译分组名与结果名
- 不要在 `Search` 中做不可中断的长时间计算
- 不要复用托盘插件（`PluginsItemInterfaceV2`）或 Shell 插件（`DApplet`）的接口
- 不要在 `Exec` 中写含空格的路径
- 不要用 `QSettings` 之外的格式写插件配置（必须是 INI `.conf`）
