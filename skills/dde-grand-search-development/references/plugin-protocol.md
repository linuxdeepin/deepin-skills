# 搜索插件接口规范（V1.0）

本文档定义扩展搜索插件必须实现的 DBus 接口与 JSON 数据格式。当前 daemon 仅支持 **V1.0**。

## 1. 接口总览

插件需在会话总线上注册 DBus 服务与对象，并实现三个方法：

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `Search` | `String json` | `String json` | 执行搜索，返回搜索结果 |
| `Stop` | `String json` | `Boolean` | 中断搜索任务 |
| `Action` | `String json` | `Boolean` | 对搜索结果执行操作 |

方法名大小写敏感，必须为 `Search`/`Stop`/`Action`。DBus 类型签名必须为 `s→s`、`s→b`、`s→b`。

### 接口 XML

项目提供接口描述文件 `src/dde-grand-search-daemon/searchplugin/interface/abstract/com.deepin.dde.grandsearch.searchplugin.xml`，也可直接使用模板 [assets/dbus/com.deepin.dde.grandsearch.searchplugin.xml](../assets/dbus/com.deepin.dde.grandsearch.searchplugin.xml)：

```xml
<!DOCTYPE node PUBLIC "-//freedesktop//DTD D-BUS Object Introspection 1.0//EN"
  "http://www.freedesktop.org/standards/dbus/1.0/introspect.dtd">
<node>
  <interface name="com.deepin.dde.GrandSearch.SearchPlugin">
    <method name="Search">
      <arg type="s" direction="out"/>
      <arg name="json" type="s" direction="in"/>
    </method>
    <method name="Action">
      <arg type="b" direction="out"/>
      <arg name="json" type="s" direction="in"/>
    </method>
    <method name="Stop">
      <arg type="b" direction="out"/>
      <arg name="json" type="s" direction="in"/>
    </method>
  </interface>
</node>
```

> XML 中的接口名 `com.deepin.dde.GrandSearch.SearchPlugin` 只是**默认值**。插件可以使用自定义接口名，但必须与 `.conf` 的 `DBusInterface` 字段完全一致。用 `qdbusxml2cpp` 生成 Adaptor 时注意同步修改接口名。

## 2. 版本一致性

插件开发中必须保证以下三处版本一致，任一不一致都会导致插件不可用：

| 位置 | 要求 |
|------|------|
| `.conf` 的 `InterfaceVersion` | `1.0`，否则 `PluginLoader` 跳过该插件 |
| 插件 DBus 接口实现 | 按 V1.0 提供 `Search`/`Stop`/`Action` |
| JSON 报文中的 `ver` | 请求与结果都必须为 `"1.0"` |

特别注意**结果 JSON 的 `ver`**：daemon 在 `ConvertorV1_0::result` 中校验 `ver`，不匹配时整个结果集被丢弃，日志中只有一条 `Invalid result format from plugin`。

## 3. Search 接口

### 3.1 签名

```
Search (String json) ↦ (String json)
```

### 3.2 输入

```json
{
    "ver": "1.0",
    "mID": "202110000000",
    "cont": "dde"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `ver` | String | 版本号，固定 `"1.0"` |
| `mID` | String | 任务号，标识一次搜索，全局唯一 |
| `cont` | String | 搜索关键词 |

### 3.3 输出

```json
{
    "ver": "1.0",
    "mID": "202110000000",
    "cont": [
        {
            "group": "应用商店",
            "items": [
                {
                    "item": "dde-desktop",
                    "name": "桌面",
                    "icon": "/usr/share/icons/hicolor/48x48/apps/desktop.svg",
                    "type": "application/appstore-app"
                },
                {
                    "item": "dde-file-manager",
                    "name": "文件管理器",
                    "icon": "dde-file-manager",
                    "type": "application/appstore-app"
                }
            ]
        }
    ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `ver` | String | 是 | 固定 `"1.0"`，必须与输入一致 |
| `mID` | String | 是 | 与输入中的 `mID` 保持一致 |
| `cont` | Array | 是 | 分组列表，支持多个分组；无结果时传空数组 `[]` |
| `cont[].group` | String | 是 | 分组名，界面展示用，**需插件自行国际化** |
| `cont[].items` | Array | 是 | 该组下的结果项列表 |
| `cont[].items[].item` | String | 是 | 结果项标识，组内唯一，不展示 |
| `cont[].items[].name` | String | 是 | 结果项名称，界面展示，**需插件自行国际化** |
| `cont[].items[].icon` | String | 否 | 图标路径或主题图标名；为空用默认图标 |
| `cont[].items[].type` | String | 是 | 项目类型，遵循 MIME type 规范，用于匹配预览插件 |

**无结果时返回空数组**，不要省略 `cont` 字段，也不要返回 `null`：

```json
{"ver": "1.0", "mID": "202110000000", "cont": []}
```

### 3.4 可中断要求

`Search` 必须可被 `Stop` 中断：`Stop` 被调用后，正在执行的 `Search` 应尽快返回（返回已完成的部分结果或空结果均可）。

推荐做法：

- 用原子标志（`std::atomic_bool` / `QAtomicInt`）记录每个任务号的中断状态；
- 搜索循环中周期性检查该标志并提前返回；
- 不要用「阻塞等待直到全部结果算完」的实现，否则界面会一直卡在搜索态直到 25 秒超时。

### 3.5 性能要求

- daemon 超时为 **25 秒**，超时按无结果处理，插件不会收到通知。
- `Search` 在 daemon 侧是异步调用，但仍应避免长时间占用主线程导致 DBus 无法响应 `Stop`。
- 结果不宜过多：跨组累计超过 100 项会被截断，建议只返回最相关的少量结果。

## 4. Stop 接口

### 4.1 签名

```
Stop (String json) ↦ (Boolean)
```

### 4.2 输入

```json
{
    "ver": "1.0",
    "mID": "202110000000"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `ver` | String | 固定 `"1.0"` |
| `mID` | String | 与对应 `Search` 的任务号一致 |

### 4.3 输出

- `true`：停止成功
- `false`：停止失败

> daemon 只在自身认为搜索仍在进行时才会调用 `Stop`（`m_searching` 为真）。若 `Search` 已返回，`Stop` 不会被调用，插件也不应依赖它做资源清理。

## 5. Action 接口

### 5.1 签名

```
Action (String json) ↦ (Boolean)
```

### 5.2 输入

```json
{
    "ver": "1.0",
    "action": "openitem",
    "item": "dde-desktop"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `ver` | String | 固定 `"1.0"` |
| `action` | String | 操作类型，当前仅 `"openitem"` |
| `item` | String | 结果项标识，与 `Search` 结果中的 `item` 一致 |

### 5.3 输出

- `true`：操作成功
- `false`：操作失败

### 5.4 定位结果的两种做法

`Action` 由 daemon 新建的临时 `PluginLiaison` 发起，与搜索时的实例不同。插件定位结果项有两种策略：

| 策略 | 适用场景 | 做法 |
|------|----------|------|
| 内存缓存 | Auto/Trigger 模式，进程常驻 | 以 `mID` 或 `item` 为键缓存结果，`Action` 时查表 |
| 自描述 `item` | 进程可能已退出，或 Manual 模式由外部宿主管理 | 把定位所需信息编码进 `item`，例如 `file:/path/to/x.pdf`、`app:org.example.App`、`calc:(3+4)*2` |

推荐优先使用自描述 `item`，因为它不依赖进程生命周期，也便于日志排查。若使用内存缓存，需加锁保护（`Search` 与 `Action` 可能来自不同线程）。

## 6. 协议常量

常量定义在 daemon 源码 `utils/searchpluginprotocol.h`，插件可自行定义同名常量以避免硬编码字符串：

```cpp
// 协议字段名
#define PLUGININTERFACE_PROTOCOL_VERSION     "ver"       // 版本号
#define PLUGININTERFACE_PROTOCOL_MISSIONID   "mID"       // 任务号
#define PLUGININTERFACE_PROTOCOL_CONTENT     "cont"      // 搜索内容/结果
#define PLUGININTERFACE_PROTOCOL_GROUP       "group"     // 分组名
#define PLUGININTERFACE_PROTOCOL_ITEMS       "items"     // 项目列表
#define PLUGININTERFACE_PROTOCOL_ITEM        "item"      // 项目标识
#define PLUGININTERFACE_PROTOCOL_NAME        "name"      // 项目名称
#define PLUGININTERFACE_PROTOCOL_TYPE        "type"      // 项目类型
#define PLUGININTERFACE_PROTOCOL_ICON        "icon"      // 项目图标
#define PLUGININTERFACE_PROTOCOL_ACTION      "action"    // 操作类型

// 操作类型值
#define PLUGININTERFACE_PROTOCOL_ACTION_OPEN "openitem"  // 打开操作
```

## 7. 扩展属性（仅内置搜索器）

daemon 源码 `global/builtinsearch.h` 中定义了结果项的扩展属性，通过 `MatchedItem.extra`（`QVariantHash`）传递：

| 属性 | 字段名 | 说明 |
|------|--------|------|
| 显示等级 | `itemLevel` | 1/2/3，控制组内显示顺序 |
| 权重计算方法 | `weightMethod` | `localFileMethod`、`desktopAppMethod`、`settingMethod` |
| 权重值 | `itemWeight` | 数值，用于排序 |
| 拖尾信息 | `itemTailer` | 结果显示在下方的附加信息 |
| 修改时间 | `itemModifiedTime` | 文件修改时间 |
| 匹配上下文 | `itemMatchedContext` | 匹配到的具体信息 |
| 匹配关键词 | `itemKeywords` | 匹配关键词列表 |

> **第三方插件无法设置这些属性**：V1.0 协议的 `cont[].items[]` 只解析 `item`/`name`/`icon`/`type` 四个字段，`extra` 不会被填充。插件若需要展示附加信息（如「点击复制到剪贴板」这类提示），只能写进 `name` 文本本身。这是设计限制，不是 bug。

## 8. 结果项与预览的配合

`type` 字段决定点击结果后使用哪个预览插件。前端匹配逻辑（`PreviewPluginManager`）：

1. 取 `item.type` 作为 MIME type；
2. 与各预览插件 `.conf` 中 `Mimetypes`（**以 `:` 分隔**，支持 `text/*` 形式的前缀通配）逐一比较，忽略大小写；
3. 命中则加载对应预览插件；未命中则使用通用预览。

因此：

- 搜索结果若是文件，`type` 应填该文件的真实 MIME type（如 `application/pdf`、`text/plain`），这样能直接复用内置的文本/图片/PDF/音视频预览插件；
- 搜索结果不是文件（如应用、设置项、计算式），`type` 填一个语义化自定义值（如 `calculator/result`、`application/appstore-app`），界面会走通用预览；
- 不要留空 `type`——留空会导致该结果项被 daemon 直接丢弃。

## 9. 完整 JSON 往返示例

以「1+2*3」为例：

**daemon → 插件**

```json
{"ver":"1.0","mID":"task-001","cont":"1+2*3"}
```

**插件 → daemon**

```json
{"ver":"1.0","mID":"task-001","cont":[{"group":"计算器","items":[{"item":"calc-1+2*3","name":"1+2*3 = 7","icon":"accessories-calculator","type":"calculator/result"}]}]}
```

**用户点击结果时 daemon → 插件**

```json
{"ver":"1.0","action":"openitem","item":"calc-1+2*3"}
```

**插件 → daemon**

```
true
```
