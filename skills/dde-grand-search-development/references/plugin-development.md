# 插件开发完整流程

本文档给出从零创建一个扩展搜索插件的完整步骤：分配 DBus 信息、实现接口、编写配置、构建安装、重启验证、打包发布。

## 1. 确定插件信息

先为插件分配一组全局唯一的信息，后续所有文件都必须与之一致：

```
插件名 (Name)     : com.example.MySearch
DBus 服务名        : com.example.MySearch
DBus 对象路径      : /com/example/MySearch
DBus 接口名        : com.example.MySearch.SearchPlugin
接口版本           : 1.0
运行模式           : Auto / Manual / Trigger
```

命名建议：`Name` 使用 `com.<公司>.<应用>.<功能>` 形式，DBus 对象路径用 `/` 分隔的同名形式。检查 `Name` 是否与内置搜索项冲突，见 [plugin-config.md](plugin-config.md#5-内置搜索项冲突)。

## 2. 创建工程结构

推荐目录结构（与 `examples/calculator-search-plugin` 一致）：

```
my-search-plugin/
├── CMakeLists.txt              # 构建配置
├── main.cpp                    # 入口，DBus 服务注册
├── mysearcher.h / .cpp         # 搜索逻辑
├── searchpluginadaptor.h / .cpp# DBus Adaptor
├── my-search.conf.in           # 配置模板（CMake 生成 .conf）
└── debian/                     # 打包文件
```

可直接复制 [assets/](../assets) 下的模板作为起点。

## 3. 实现 DBus Adaptor

### 3.1 手写 Adaptor（推荐，无需额外构建步骤）

继承 `QDBusAbstractAdaptor`，用 `Q_CLASSINFO` 声明接口名与 Introspection 元数据：

```cpp
class SearchPluginAdaptor : public QDBusAbstractAdaptor
{
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "com.example.MySearch.SearchPlugin")
    Q_CLASSINFO("D-Bus Introspection", ""
        "  <interface name=\"com.example.MySearch.SearchPlugin\">\n"
        "    <method name=\"Search\">\n"
        "      <arg type=\"s\" direction=\"out\"/>\n"
        "      <arg name=\"json\" type=\"s\" direction=\"in\"/>\n"
        "    </method>\n"
        "    <method name=\"Action\">\n"
        "      <arg type=\"b\" direction=\"out\"/>\n"
        "      <arg name=\"json\" type=\"s\" direction=\"in\"/>\n"
        "    </method>\n"
        "    <method name=\"Stop\">\n"
        "      <arg type=\"b\" direction=\"out\"/>\n"
        "      <arg name=\"json\" type=\"s\" direction=\"in\"/>\n"
        "    </method>\n"
        "  </interface>\n"
        "")
public:
    explicit SearchPluginAdaptor(QObject *parent = nullptr);

public slots:
    QString Search(const QString &json);
    bool Stop(const QString &json);
    bool Action(const QString &json);
};
```

Adaptor 的方法名必须与 DBus 方法名完全一致（`Search`/`Stop`/`Action`，首字母大写）。

完整模板：[assets/src/searchpluginadaptor.h](../assets/src/searchpluginadaptor.h)、[assets/src/searchpluginadaptor.cpp](../assets/src/searchpluginadaptor.cpp)。

### 3.2 用 qdbusxml2cpp 生成

```bash
qdbusxml2cpp -a searchpluginadaptor -c SearchPluginAdaptor \
  com.deepin.dde.grandsearch.searchplugin.xml
```

生成后需检查：

- 接口名与 `.conf` 的 `DBusInterface` 一致（XML 中默认是 `com.deepin.dde.GrandSearch.SearchPlugin`，如使用自定义接口名要改）；
- 生成的是 Adaptor（`-a`），不是 Interface（`-p`）——插件侧需要 Adaptor。

> 使用生成的 Adaptor 时注意：`qdbusxml2cpp` 生成的 Adaptor 会自己实现方法转发，不要再额外写一层手工转发。

## 4. 实现搜索逻辑

搜索逻辑的核心是三件事：解析输入 JSON、执行搜索、构造结果 JSON。要点：

| 要点 | 说明 |
|------|------|
| 校验 `ver` | 输入 `ver` 不是 `"1.0"` 时返回空结果，不要继续处理 |
| 校验 `mID` | 为空时返回空结果（daemon 侧也会丢弃） |
| 关键词预过滤 | 先用正则/规则快速排除不可能匹配的输入，避免无谓计算 |
| 可中断 | 用原子标志记录中断，搜索循环中周期检查 |
| 结果上限 | 只返回最相关的少量结果（跨组累计 100 项上限） |
| 必填字段 | `item`/`name`/`type` 三个字段必须非空，否则结果项被丢弃 |
| 结果 `ver` | 必须回填 `"1.0"`，否则整个结果集被丢弃 |

结果构造示例：

```cpp
QJsonObject root;
root["ver"] = "1.0";
root["mID"] = mID;

QJsonArray contents;
QJsonObject group;
group["group"] = QCoreApplication::translate("MyPlugin", "My Plugin");

QJsonArray items;
QJsonObject item;
item["item"] = itemKey;      // 结果项标识，Action 时原样回传
item["name"] = displayName;  // 界面展示，需国际化
item["icon"] = iconName;     // 图标路径或主题图标名，可为空
item["type"] = mimeType;     // MIME type 规范，决定预览插件匹配
items.append(item);

group["items"] = items;
contents.append(group);
root["cont"] = contents;

return QJsonDocument(root).toJson(QJsonDocument::Compact);
```

完整骨架：[assets/src/searcher.cpp](../assets/src/searcher.cpp)。

## 5. 注册 DBus 服务

入口函数中注册服务与对象。**必须使用会话总线**：

```cpp
int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    app.setApplicationName("my-search-plugin");

    MySearcher searcher;
    SearchPluginAdaptor adaptor(&searcher);   // Adaptor 必须是导出对象的子对象

    QDBusConnection connection = QDBusConnection::sessionBus();
    if (!connection.registerService("com.example.MySearch")) {
        qCritical("Failed to register DBus service");
        return 1;
    }
    if (!connection.registerObject("/com/example/MySearch", &searcher)) {
        qCritical("Failed to register DBus object");
        return 1;
    }

    return app.exec();
}
```

三个关键点：

1. `adaptor` 的父对象必须是 `searcher`（导出对象），否则 Adaptor 不会随对象一起导出，DBus 上找不到 `Search` 方法；
2. 服务名与对象路径必须与 `.conf` 完全一致；
3. `registerService` 失败通常意味着已有同名服务在运行（例如上一个实例没退出），此时应退出而不是继续运行。

完整模板：[assets/src/main.cpp](../assets/src/main.cpp)。

## 6. CMake 工程配置

关键要求：

- Qt5/Qt6 自动检测（`Core`、`Gui`、`DBus`，若只用到剪贴板等 GUI 能力才需要 `Gui`）；
- 安装可执行文件到 `${CMAKE_INSTALL_FULL_LIBDIR}/dde-grand-search-daemon/plugins/searcher/`；
- 用 `configure_file` 从 `.conf.in` 生成 `.conf`，把 `Exec` 的绝对路径注入进去；
- 一并安装 `.conf` 到同一目录。

```cmake
include(GNUInstallDirs)

if(NOT DEFINED PLUGIN_INSTALL_DIR)
    set(PLUGIN_INSTALL_DIR
        ${CMAKE_INSTALL_FULL_LIBDIR}/dde-grand-search-daemon/plugins/searcher)
endif()

install(TARGETS ${PROJECT_NAME} RUNTIME DESTINATION ${PLUGIN_INSTALL_DIR})

set(PLUGIN_EXEC_PATH "${PLUGIN_INSTALL_DIR}/${PROJECT_NAME}")
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/my-search.conf.in
               ${CMAKE_CURRENT_BINARY_DIR}/my-search.conf @ONLY)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/my-search.conf
        DESTINATION ${PLUGIN_INSTALL_DIR})
```

完整模板：[assets/cmake/CMakeLists.txt](../assets/cmake/CMakeLists.txt)。

> `CMAKE_INSTALL_FULL_LIBDIR` 会自动展开为 `/usr/lib/<arch>`（x86_64 下即 `/usr/lib/x86_64-linux-gnu`），这正是 daemon 期望的 `$PLATFORM` 路径。不要手写 `/usr/lib/x86_64-linux-gnu`。

## 7. 构建与安装

### 7.1 CMake 开发构建

```bash
cmake -B build -DCMAKE_INSTALL_PREFIX=/usr
cmake --build build -j$(nproc)
sudo cmake --build build --target install
```

安装后目录内容：

```
/usr/lib/x86_64-linux-gnu/dde-grand-search-daemon/plugins/searcher/
├── my-search-plugin       # 可执行文件
└── my-search.conf         # 插件配置
```

### 7.2 编译依赖

```bash
# Qt6（deepin/UOS v25 默认）
sudo apt install cmake qt6-base-dev qt6-base-dev-tools

# Qt5
sudo apt install cmake qtbase5-dev qtbase5-dev-tools
```

运行依赖：`dde-grand-search`。

## 8. 重启 daemon

`.conf` 只在 daemon 启动时读取，安装或修改配置后必须重启：

```bash
sudo systemctl restart dde-grand-search-daemon
```

或手动重启：

```bash
killall dde-grand-search-daemon
dde-grand-search-daemon &
```

> 开发阶段可以先用 `killall` + 前台运行 daemon 的方式，便于直接观察日志输出。

## 9. 验证

按「由内到外」的顺序验证，逐层排除问题：

**第一步：确认插件被发现**

```bash
QT_LOGGING_RULES="logDaemon.debug=true" dde-grand-search-daemon
```

在日志中查找 `Added plugin - File: ... Name: ... Mode: ...`。若没有这一行，说明配置未通过校验，检查路径、后缀、必填字段、`Name` 是否与内置项冲突。

**第二步：确认 DBus 服务已注册**

```bash
# 查看服务是否在会话总线上
dbus-send --session --print-reply --dest=org.freedesktop.DBus \
  /org/freedesktop/DBus org.freedesktop.DBus.ListNames | grep MySearch

# 查看对象与接口
d-feet        # 图形化浏览会话总线
```

**第三步：单独验证接口**

```bash
dbus-send --session --print-reply \
  --dest=com.example.MySearch \
  /com/example/MySearch \
  com.example.MySearch.SearchPlugin.Search \
  "string:{\"ver\":\"1.0\",\"mID\":\"test001\",\"cont\":\"关键词\"}"
```

应返回符合 V1.0 规范的 JSON。此步失败说明接口实现或接口名有问题，与 daemon 无关。

**第四步：在搜索界面验证**

打开全局搜索，输入能命中插件的关键词，确认：

- 结果出现在正确的分组下；
- 图标显示正常；
- 点击结果触发预期行为；
- 快速连续输入时旧结果被正确中断（不出现错乱结果）。

**第五步：验证生命周期**

- Auto 模式：`ps` 确认插件进程存在；`kill` 掉进程后确认 daemon 自动重启（High/Middle）；
- Trigger 模式：确认插件未运行时会话总线上的服务调用能自动拉起进程。

## 10. Debian 打包

插件作为独立包发布。参考模板：[assets/debian/control](../assets/debian/control)、[assets/debian/rules](../assets/debian/rules)、[assets/debian/changelog](../assets/debian/changelog)。

`debian/control` 要点：

```
Build-Depends: debhelper (>= 11),
               cmake,
               qt6-base-dev | qtbase5-dev,
               qt6-base-dev-tools | qtbase5-dev-tools

Package: my-search-plugin
Architecture: any
Depends: ${shlibs:Depends}, ${misc:Depends},
         dde-grand-search
```

`debian/rules` 使用 cmake 构建系统：

```make
#!/usr/bin/make -f
%:
	dh $@ --buildsystem=cmake
```

构建：

```bash
sudo apt build-dep .
dpkg-buildpackage -uc -us -nc
sudo dpkg -i my-search-plugin_1.0.0_*.deb
```

> 打包后仍需重启 daemon 才能加载插件；若希望在安装时自动生效，可在 `debian/postinst` 中加入重启逻辑，但要考虑安装时 daemon 可能未运行的场景。

## 11. 开发检查清单

提交前逐项核对：

- [ ] `.conf` 的 `Name` 不与内置搜索项冲突，且在系统内唯一
- [ ] `InterfaceVersion`、接口实现、JSON `ver` 三处都是 `1.0`
- [ ] `DBusService`/`DBusAddress`/`DBusInterface` 与代码注册完全一致
- [ ] 注册在会话总线（`sessionBus()`），不是系统总线
- [ ] Adaptor 是导出对象的子对象
- [ ] `Auto` 模式的 `Exec` 路径存在且可执行，路径中无空格
- [ ] 结果 JSON 中 `item`/`name`/`type` 均非空，`ver` 回填 `1.0`
- [ ] 分组名与结果名已按系统语言本地化
- [ ] `Search` 可被 `Stop` 中断，不会阻塞超过 25 秒
- [ ] 安装路径为 `${CMAKE_INSTALL_FULL_LIBDIR}/dde-grand-search-daemon/plugins/searcher/`
- [ ] 已重启 daemon 并完成验证，或明确说明未验证项
