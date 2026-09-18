# 调试与故障排查

插件问题的典型表现是「界面里看不到我的结果」。排查的关键是**分层定位**：先确认插件被发现，再确认 DBus 服务可用，最后确认结果 JSON 合法。

## 1. 日志

daemon 使用 `QLoggingCategory` 管理日志，调试时开启详细输出：

```bash
QT_LOGGING_RULES="logDaemon.debug=true" dde-grand-search-daemon
```

插件侧也建议使用 `QLoggingCategory` 并支持运行时开关：

```cpp
Q_LOGGING_CATEGORY(logMyPlugin, "myplugin.search")

// main() 中允许通过环境变量开启
QLoggingCategory::setFilterRules("myplugin.search.debug=true");
```

开发时把插件日志写到 stderr，由 daemon 的 `QProcess` 继承（Auto 模式）或直接在当前终端可见（手动启动）。

## 2. 分层排查流程

```
① 插件是否被发现？
   daemon 日志搜索 "Added plugin"
   ├─ 无 → 检查 conf 路径/后缀/必填字段/Name 冲突
   └─ 有 ↓
② 插件进程/服务是否就绪？
   dbus-send ListNames | grep <DBusService>
   ├─ 无 → 检查 Exec 路径、进程是否崩溃、Trigger 的 .service 文件
   └─ 有 ↓
③ 接口是否可调用？
   dbus-send 手动调 Search
   ├─ 报错 no such method / Unknown interface → 接口名与 conf 不一致
   ├─ 报错 Unknown object → 对象路径不一致
   └─ 正常返回 ↓
④ 返回的 JSON 是否合法？
   对照 V1.0 规范逐字段核对
   ├─ ver 不是 1.0 → 整个结果被丢弃
   ├─ item/name/type 为空 → 该结果项被丢弃
   └─ 合法 ↓
⑤ daemon 是否收到结果？
   daemon 日志搜索 "Invalid result format" / "Received search reply"
⑥ 前端是否展示？
   检查 type 与预览插件匹配、分组名是否为空
```

## 3. DBus 调试命令

### 3.1 测试 Search 接口

```bash
dbus-send --session --print-reply \
  --dest=com.example.MySearch \
  /com/example/MySearch \
  com.example.MySearch.SearchPlugin.Search \
  "string:{\"ver\":\"1.0\",\"mID\":\"test001\",\"cont\":\"1+2*3\"}"
```

### 3.2 测试 Stop 接口

```bash
dbus-send --session --print-reply \
  --dest=com.example.MySearch \
  /com/example/MySearch \
  com.example.MySearch.SearchPlugin.Stop \
  "string:{\"ver\":\"1.0\",\"mID\":\"test001\"}"
```

### 3.3 测试 Action 接口

```bash
dbus-send --session --print-reply \
  --dest=com.example.MySearch \
  /com/example/MySearch \
  com.example.MySearch.SearchPlugin.Action \
  "string:{\"ver\":\"1.0\",\"action\":\"openitem\",\"item\":\"result-0\"}"
```

### 3.4 查看服务与对象

```bash
# 服务是否注册
dbus-send --session --print-reply --dest=org.freedesktop.DBus \
  /org/freedesktop/DBus org.freedesktop.DBus.ListNames | grep -i mysearch

# 查看对象的接口与方法签名
dbus-send --session --print-reply --dest=com.example.MySearch \
  /com/example/MySearch org.freedesktop.DBus.Introspectable.Introspect
```

图形化工具 `d-feet` 可以直观浏览会话总线上的服务、对象与方法：

```bash
d-feet
```

> 用 `d-feet` 或 `Introspect` 检查时，重点核对**方法签名**是否为 `Search(s)→s`、`Stop(s)→b`、`Action(s)→b`。签名不符时 daemon 调用会失败。

## 4. 常见问题对照表

| 现象 | 可能原因 | 处理 |
|------|----------|------|
| 插件未被加载 | 配置文件路径不正确 | 确认文件位于 `/usr/lib/$PLATFORM/dde-grand-search-daemon/plugins/searcher/` 且后缀为 `.conf` |
| 插件未被加载 | 名称与内置搜索项冲突 | 修改 `Name`，避开内置名称列表 |
| 插件未被加载 | `InterfaceVersion` 不受支持 | 确认版本号为 `1.0` |
| 插件未被加载 | 缺少必填字段 | 检查 `Name`、`DBusService`、`DBusAddress`、`DBusInterface`、`InterfaceVersion` |
| 插件未被加载 | 根节点不是 `[Grand Search]` | 修正 INI 根节点名 |
| 插件未被加载 | 目录不可读 / 权限问题 | 检查插件目录与文件权限 |
| 改配置后无变化 | 未重启 daemon | `systemctl restart dde-grand-search-daemon` |
| Auto 插件未启动 | `Exec` 为空或路径错误 | 检查可执行文件存在且有执行权限 |
| Auto 插件未启动 | `Exec` 路径含空格 | `Exec` 按空格拆分，路径中不能有空格 |
| Auto 插件启动后立即退出 | 程序启动失败或依赖缺失 | 手动执行该程序查看报错；检查动态库依赖 |
| Auto 插件反复重启 | 程序崩溃 | 查看插件日志；重启超过 3 次后 daemon 放弃 |
| Trigger 插件未拉起 | 缺少 `.service` 文件 | 安装到 `/usr/share/dbus-1/services/` |
| Trigger 插件未拉起 | `.service` 中 `Exec` 路径错误 | 修正为可执行文件绝对路径 |
| 搜索无结果 | DBus 服务未注册成功 | 用 `dbus-send`/`d-feet` 检查服务 |
| 搜索无结果 | 接口名与 conf 不一致 | 核对 `DBusInterface` 与 Adaptor 的 `Q_CLASSINFO` |
| 搜索无结果 | 结果 JSON 的 `ver` 不是 `1.0` | 回填 `"1.0"`；daemon 日志有 `Invalid result format` |
| 搜索无结果 | `item`/`name`/`type` 为空 | 三个字段必须非空 |
| 搜索无结果 | 分组名 `group` 为空 | 空分组被整体跳过 |
| 搜索结果被截断 | 跨组累计超过 100 项 | daemon 端限制，插件应少返回、返回最相关的 |
| 搜索超时 | 插件响应超过 25 秒 | 优化性能，保证可中断 |
| 结果点击无反应 | `item` 与 Action 传入值不匹配 | 保证 `item` 组内唯一且可自描述 |
| 结果点击无反应 | Action 依赖已丢失的内存状态 | 改用自描述 `item` |
| 结果图标不显示 | `icon` 路径不存在或主题名错误 | 用绝对路径或确认主题中存在该图标名 |
| 结果落到通用预览 | `type` 不是有效 MIME type | 文件类结果填真实 MIME type |

## 5. 排查技巧

### 5.1 先隔离插件与 daemon

`dbus-send` 直接调用插件接口，可以完全绕开 daemon。如果这一步正常但界面无结果，问题一定在**结果 JSON 格式**或**conf 配置**上，而不在插件业务逻辑里。这一步能省下大量时间。

### 5.2 手动前台运行 daemon

```bash
killall dde-grand-search-daemon
QT_LOGGING_RULES="logDaemon.debug=true" dde-grand-search-daemon
```

前台运行时可以直接看到插件加载、激活、调用、解析的全过程日志。

### 5.3 手动前台运行插件

Auto 模式下插件由 daemon 拉起，stderr 不易观察。开发时可以先手动运行插件进程，再用 `Manual` 模式的思路单独验证：

```bash
# 终端 1
./my-search-plugin

# 终端 2
dbus-send --session --print-reply --dest=com.example.MySearch \
  /com/example/MySearch com.example.MySearch.SearchPlugin.Search \
  "string:{\"ver\":\"1.0\",\"mID\":\"t1\",\"cont\":\"test\"}"
```

### 5.4 检查进程生命周期

```bash
# 插件进程是否存在
ps aux | grep my-search-plugin

# 守护重启是否生效：kill 后观察是否被拉起
kill <pid>
```

### 5.5 核对结果 JSON

把 `dbus-send` 返回的 JSON 用 `jq` 格式化后逐字段核对，比在界面里猜要快得多：

```bash
dbus-send ... | sed 's/.*string "//; s/"$//' | jq .
```

## 6. 日志关键字速查

| 关键字 | 含义 |
|--------|------|
| `Added plugin - File: ...` | 插件配置解析成功 |
| `Failed to read plugin configuration` | conf 解析失败（字段缺失/根节点错误） |
| `Plugin conflicts with built-in search` | `Name` 与内置搜索项冲突 |
| `Duplicate plugin name found` | `Name` 重复 |
| `Unsupported interface version` | `InterfaceVersion` 不受支持 |
| `Starting program - Name: ...` | Auto 插件进程启动 |
| `Auto-restarting watched process` | 守护进程自动重启 |
| `Too many failures` | 重启超过 3 次，daemon 放弃 |
| `Received search reply from plugin` | 收到插件结果 |
| `Invalid result format from plugin` | 结果 JSON 解析失败（`ver`/`mID` 问题） |
| `Search error from plugin` | DBus 调用报错（接口名/服务名问题） |
| `Search already in progress` | 上一次搜索未结束，新搜索被跳过 |
| `Worker timeout - Name: ...` | 25 秒超时 |
