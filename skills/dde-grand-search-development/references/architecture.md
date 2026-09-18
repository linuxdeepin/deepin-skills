# 全局搜索架构与插件集成点

本文档描述 `dde-grand-search` 的整体架构、daemon 内部与插件相关的模块职责，以及一次搜索从发起到结果展示的完整流转。

## 1. 进程与角色

| 组件 | 进程/形态 | 职责 |
|------|-----------|------|
| `dde-grand-search` | 前端 GUI 应用 | 搜索输入框、结果分组展示、预览、点击打开 |
| `dde-grand-search-daemon` | 后端常驻进程 | 加载搜索项、调度搜索任务、聚合结果、转发操作 |
| 内置搜索器 | daemon 内部类 | 文件、应用、控制中心设置、Web、语义、OCR、全文 |
| **扩展搜索插件** | 独立 DBus 服务 | 本 skill 关注对象，提供 `Search`/`Stop`/`Action` |
| 预览插件 | daemon/前端加载的 `.so` | 按 MIME type 提供结果预览界面，不属于本 skill |

前端与 daemon 之间通过会话总线上的 `com.deepin.dde.GrandSearch` 交互；daemon 与扩展插件之间同样通过会话总线，但接口是插件自己声明的服务名与接口名。

## 2. 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                  全局搜索前端 (dde-grand-search)              │
│                    ┌─────────────────────┐                   │
│                    │   搜索结果展示界面    │                   │
│                    └─────────┬───────────┘                   │
└──────────────────────────────┼──────────────────────────────┘
                               │ DBus (com.deepin.dde.GrandSearch)
┌──────────────────────────────┼──────────────────────────────┐
│                全局搜索后端 (dde-grand-search-daemon)         │
│                    ┌─────────┴───────────┐                   │
│                    │   MainController     │                   │
│                    │   (搜索任务调度)     │                   │
│                    └─────────┬───────────┘                   │
│              ┌───────────────┼───────────────┐               │
│              ▼               ▼               ▼               │
│      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐      │
│      │  内置搜索器   │ │  扩展搜索器   │ │  预览插件     │      │
│      │  (文件/应用   │ │ (ExtendSea-  │ │ (preview)    │      │
│      │   /设置/Web)  │ │   rcher)     │ │              │      │
│      └──────────────┘ └──────┬───────┘ └──────────────┘      │
│                             │                                │
│                    ┌────────┴──────────┐                     │
│                    │  PluginManager     │                     │
│                    │  (插件管理/加载)    │                     │
│                    └────────┬──────────┘                     │
│                             │                                │
│              ┌──────────────┼──────────────┐                 │
│              ▼              ▼              ▼                 │
│      ┌──────────────┐┌──────────────┐┌──────────────┐        │
│      │PluginLoader  ││PluginProcess ││PluginLiaison │        │
│      │(读取conf配置) ││(进程管理)     ││(DBus通信)     │        │
│      └──────────────┘└──────────────┘└──────────────┘        │
└──────────────────────────────┬──────────────────────────────┘
                               │ DBus (插件自定义服务名)
┌──────────────────────────────┼──────────────────────────────┐
│                     第三方搜索插件                            │
│              ┌───────────────┴───────────────┐              │
│              │   插件进程 (独立 DBus 服务)      │              │
│              │   ┌─────────────────────────┐ │              │
│              │   │  Search()  搜索接口      │ │              │
│              │   │  Stop()    停止接口      │ │              │
│              │   │  Action()  操作接口      │ │              │
│              │   └─────────────────────────┘ │              │
│              └───────────────────────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

## 3. daemon 内部模块职责

| 模块 | 源文件 | 职责 |
|------|--------|------|
| `PluginManager` | `searchplugin/pluginmanager.cpp` | 插件加载总入口：初始化数据协议、读 conf、把 Auto 插件交给进程管理、按优先级激活 |
| `PluginLoader` | `searchplugin/loader/pluginloader.cpp` | 扫描插件目录下 `*.conf`，解析并校验字段，过滤与内置项冲突或重名的插件 |
| `PluginProcess` | `searchplugin/process/pluginprocess.cpp` | Auto 模式插件的进程启动、守护重启、稳定性检查与退出 |
| `ExtendSearcher` | `searcher/extend/extendsearcher.cpp` | 把每个扩展插件包装成一个搜索项，负责激活（进程或 DBus Ping）与转发 Action |
| `ExtendWorker` | `searcher/extend/extendworker.cpp` | 单次搜索的执行单元，持有 `PluginLiaison`，管理 25s 超时与中断 |
| `PluginLiaison` | `searchplugin/pluginliaison.cpp` | DBus 调用与结果解析：构造请求 JSON、异步调用、在子线程解析结果、发信号 |
| `DataConvertor` + `ConvertorV1_0` | `searchplugin/convertors/` | 协议编解码：请求 → JSON、结果 JSON → `MatchedItemMap` |

## 4. 搜索流程

```
用户输入关键词
   │
   ▼
前端 → daemon：发起搜索（携带任务号 mID、关键词 cont）
   │
   ▼
MainController 创建搜索任务，遍历所有搜索项（含扩展插件）
   │
   ▼
ExtendSearcher：检查插件是否可用
   ├─ 服务已注册 → 直接搜索
   └─ 服务未注册 → 按 Mode 激活
        ├─ Auto   → PluginProcess 启动 Exec 进程
        └─ Trigger → 向插件服务发 org.freedesktop.DBus.Peer.Ping，
                    由 DBus 依据 .service 文件自动拉起
        └─ Manual → 不激活，等待外部启动
   │
   ▼
PluginLiaison::search()
   ConvertorV1_0::search 构造请求 JSON → 插件 Search(json)
   │
   ▼
插件执行搜索（须可被 Stop 中断），返回结果 JSON
   │
   ▼
PluginLiaison 收到回复 → 子线程 parseResult()
   ConvertorV1_0::result 解析 → MatchedItemMap
   │
   ▼
emit searchFinished(items) → ExtendWorker 收集 → MainController 聚合
   │
   ▼
前端分批拉取结果并展示（分组标题 + 结果列表）
```

关键细节：

- **异步**：`Search` 是异步 DBus 调用（`QDBusPendingReply`），结果在子线程解析后通过队列连接回到主线程。插件不需要额外开线程，但**不要阻塞事件循环**（同步等待、sleep、长时间独占锁都会拖慢整个搜索）。
- **超时 25 秒**：`PluginLiaison::init` 中 `setTimeout(25 * 1000)`，`ExtendWorker` 另有 25 秒单次定时器。超时按无结果处理，插件侧不会收到任何通知。
- **单次搜索互斥**：同一插件在 `m_searching` 为真时再次发起搜索会直接返回失败，因此插件必须让上一次 `Search` 结束。
- **服务延迟启动**：若发起搜索时插件服务尚未注册，daemon 会等待 `NameOwnerChanged` 信号（`PluginLiaison::ready`）后重试一次；这也是 Auto/Trigger 模式能工作的机制。

## 5. 结果流转与解析限制

插件返回的 JSON 由 `ConvertorV1_0::result` 解析，规则如下：

| 规则 | 行为 |
|------|------|
| `ver` 不等于 `"1.0"` | 转换失败，整个结果被丢弃，daemon 记 warning |
| `mID` 为空 | 转换失败，整个结果被丢弃 |
| `cont` 不是数组或缺失 | 解析为空结果（合法但无内容） |
| `cont[].group` 为空 | 该分组整体跳过 |
| `cont[].items[].item` 为空 | 该结果项跳过 |
| `cont[].items[].name` 为空 | 该结果项跳过 |
| `cont[].items[].type` 为空 | 该结果项跳过 |
| `cont[].items[].icon` 为空 | 允许，前端使用默认图标 |
| 跨所有分组累计超过 100 项 | 后续项不再解析 |

解析后每个 `MatchedItem` 的 `searcher` 字段被置为插件的 `Name`（conf 中的值），这是后续 Action 路由的唯一依据。

## 6. 结果项字段在界面上的用途

| 字段 | 界面用途 |
|------|----------|
| `group` | 分组标题。内置分组名有翻译映射；**自定义分组名原样显示**，因此插件需自行返回本地化文本 |
| `name` | 结果条目主标题，需自行本地化 |
| `icon` | 条目图标。支持绝对路径（如 `/usr/share/icons/.../x.svg`）或图标主题名（如 `dde-file-manager`）；为空用默认图标 |
| `type` | 不展示。用于匹配预览插件（`plugins/preview/`）的 `Mimetypes`；按 MIME type 规范填写 |
| `item` | 不展示。结果项标识，`Action` 时原样回传，插件据此定位是哪一个结果 |

## 7. 操作（Action）流程

```
用户在结果项上执行打开操作
   │
   ▼
前端 → daemon：OpenWithPlugin(searcher, item)
   searcher 即插件的 Name，item 即结果项中的 item
   │
   ▼
MainController::searcherAction(searcher, "openitem", item)
   │
   ▼
ExtendSearcher::action("openitem", item)
   PluginLiaison::action → Action(json)，json = {ver, action, item}
   │
   ▼
插件执行对应操作（打开文件、复制内容、跳转页面等）
```

注意：

- daemon 对 `Action` 的返回值**不做处理**（`d->m_inteface->Action(input)` 后直接返回 `true`），但插件仍应返回 `true`/`false` 以便调试与日志分析。
- `action` 当前仅约定 `"openitem"`，其他值由插件自行扩展（daemon 只会传 `openitem`）。
- `Action` 走的是新建的临时 `PluginLiaison`，与搜索时的实例不是同一个，插件不能依赖搜索期间的内存状态——**除非常驻进程**。`Auto`/`Trigger` 模式插件进程常驻时可以缓存；若进程可能已退出，应把定位结果所需信息编码进 `item` 字段。

## 8. 与其他插件体系的区别

| 体系 | 接入方式 | 加载者 |
|------|----------|--------|
| **全局搜索扩展插件** | `.conf` + 独立 DBus 服务 | `dde-grand-search-daemon` |
| 全局搜索预览插件 | `.conf` + `.so`（按 MIME type） | daemon / 前端 |
| DDE 托盘插件 | `.so` + `PluginsItemInterfaceV2` | `dde-tray-loader` |
| DDE Shell 插件 | QML/C++ 包 + `metadata.json` | dde-shell |
| DDE 控制中心插件 | `.so`/QML + 模块注册 | dde-control-center |

不要把全局搜索插件实现成 `.so` 或声明 IID；也不要在搜索插件里复用托盘/Shell 的插件接口。
