# 元数据发现与匹配

## 目录与身份

纯元数据列表或匹配可直接读取本机目录、DSG 环境配置及可用的安装文档，无需通过 `commands.md` 的运行时入口检查。若后续需要当前值、默认状态或修改，再执行该检查；失败时保留明确标为本地元数据的候选，不继续值操作。不要用 `dde-dconfig list/get` 做元数据检索。可以使用 `rg --files --hidden` 发现 JSON，用 jq 等 JSON 解析工具读取内容，不用正则代替 JSON 解析。

常见数据根为 `/usr/share/dsg`，`DSG_DATA_DIRS` 可提供按冒号分隔的数据根；每个根下追加 `configs`。部分系统另有 `/var/lib/linglong/entries/share/dsg/configs`，存在不代表配置服务一定加载。当前 shell 环境也不必然等于服务环境；来源不能核实时标明覆盖范围，不能声称全系统完整。

典型布局：

| 路径，相对于 configs | 身份 |
| --- | --- |
| `RESOURCE.json` | 公共资源；可使用空 appId，也可在指定应用上下文中解析 |
| `APP/RESOURCE.json` | 应用资源，根 subpath 为空 |
| `APP/child/RESOURCE.json` | 应用上下文的子路径 `/child`，需确认目录确为该 APP 的子路径 |
| `overrides/APP/RESOURCE/*.json` | 应用资源覆盖文件，不是新的资源 |
| `overrides/RESOURCE/*.json` | 公共资源覆盖文件 |

resourceId 为真实存在的元数据 JSON 文件名去掉 `.json`，不能从 appId 猜一个不存在的资源。appId 标识应用上下文，可以由调用方动态构造，不要求存在同名目录或已安装应用。为实际应用修改时采用该应用真正使用的 appId；不能为了调用成功随意换成 abc 等测试身份。只有用户要求独立测试上下文时才构造新的 appId。公共资源也能被应用上下文使用；用户指定应用时，要把该 appId 的公共资源回退及应用专属 override 考虑进去，不能一律改成空 appId。目录层次有歧义时结合安装布局核实，不只凭路径深度猜身份。以完整身份去重，保留来源。

元数据查找通常先应用目录，再公共目录；同一配置在请求子路径中不存在时逐级向父目录回退。根 subpath 为 `''`，非空 subpath 使用 `/child` 形式。subpath 是针对 resource 的动态覆盖上下文，不是现有文件目录的枚举清单；请求的路径可以没有对应目录，由服务按资源查找/覆盖机制处理。不要因目录不存在直接否定上下文，也不要扫描后把物理路径强行当成实际应用使用的 subpath。应用上下文未知时先核实；不要把绝对元数据文件路径作为 subpath，也不要构造含 `..` 的目标。

## 环境与应用影响范围

X11 和 Wayland 可能使用不同资源、key 或 subpath。根据入口确认的目标会话，结合 name/description、应用后端及可靠配置说明选择；不要仅因名称相似就互换，也不要凭会话类型自行拼造 `/x11` 或 `/wayland` 子路径。环境或适用关系不明时列出候选及依据，让用户选择，再读取或修改选定项。

公共资源的 appId 是影响范围选择，不是可省略的无关参数：

- 空 appId：修改公共配置上下文，所有使用该公共配置的应用都可能受影响。
- 指定 appId：在指定应用上下文中修改，可能只影响该应用；应用是否读取该上下文、覆盖关系和 Global 属性仍需考虑。
- 应用范围与用户范围是两个维度；空 appId 不等于 Global，指定 appId 也不取消 Global 可能跨用户的影响。

用户明确要求修改某应用时使用其实际 appId，不能替换成空 appId；用户明确要求公共配置/全部应用时可用空 appId，并说明共享影响。用户只说“改主题”等未指定应用范围的请求，若公共和应用上下文都合理，先让用户选择；不得默认为所有应用，也不得构造一个任意 appId 冒充所需应用。已有明确范围无需重复确认。

## 格式与字段

只把 `magic=dsg.config.meta` 且版本受支持的 JSON 当元数据；`contents` 是 key 到声明对象的映射。损坏文件、缺失 value 或不支持的版本报告为不能可靠解析。

| 字段 | 使用方式 |
| --- | --- |
| `name`、`name[...]` | 同时作为语义匹配依据，不限定语言 |
| `description`、`description[...]` | 功能、枚举、单位、生效条件等依据，与 name/key 交叉核对 |
| `value` | 用于分析声明 JSON 类型；不作为用户所需默认值或实际值的返回依据，两者以 CLI 结果为准 |
| `visibility` | 只有 `public` 纳入；缺失按 private；未知值不纳入 |
| `permissions` | 只有有效 `readwrite` 可修改；缺失按 readonly；未知值不写入 |
| `flags` | 字符串列表；`global` 表示全局项；`nooverride` 限制覆盖，不等于运行时只读；`user-public` 不替代 visibility |
| `serial` | 声明修订相关信息，不是设置值或类型 |

读取单个文件的公开项示例（仅原始元数据，尚未合成 override，不能直接当最终可写列表）：

```bash
jq 'select(.magic == "dsg.config.meta") | .contents | to_entries[]
    | select(.value.visibility == "public")
    | {key: .key, metadata: (.value | del(.value)), declaredType: (.value.value | type)}' "$meta_file"
```

## 覆盖关系

`dsg.config.override` 不能与元数据任意深度合并，也不创建独立 key。已核实的 DTK 实现只应用已有 key 的 value、serial、permissions，忽略不存在的 key；nooverride 项不接受覆盖。因此不能用 override 中的 visibility/name/flags 擅自改变基准声明。

检查数据根下 `configs/overrides` 和 `/etc/dsg/configs/overrides`，以及请求子路径和父路径。同一层的文件涉及自然数字排序（例如 2 在 10 之前），不要用普通字典序假装等价。数据根、公共/应用上下文及子路径的跨层优先级须按目标版本确定：不同实现的遍历顺序和最终应用顺序可能不同，不能直接把“/etc 总是最后”或文件名最大者当结论。

单一元数据且无适用 override 可直接判断元信息；配置值仍须经 CLI 获取。有覆盖时记录相关来源；顺序不影响结果的同值覆盖可以确定，存在冲突且目标版本规则无法核实时，展示候选并标为“覆盖关系待核实”，不宣称最终权限/默认值、不写入。不要为核实元信息改为逐项请求服务。

## 自然语言与类型

先按用户指定的应用或功能缩小范围，再检查所有相关名称和描述。跨语言语义一致即可命中；匹配不要求词面相同。显示名称并不唯一，相同 key 在不同资源中也是不同项。

- `"value": ""` 或 `"value": "color"` 是字符串，即使表示模式/枚举也不能擅自转整数。
- `"value": 0` 是数字；结合声明说明判断整数和单位。JSON 数字不保证底层整数位宽；不要把 1.0 的小数意图在格式化时无意丢掉。
- true/false 是布尔；“开启功能”对 `disableFeature` 可能意味着 false。
- 数组/对象保留结构；空数组不能证明元素类型，null 不能证明可写目标类型。约束不足时补充核实。
- 用户说“添加”需要读取当前列表后构造新列表，不能替换整个列表；替换、添加、删除不明确时询问。
- 枚举选项只能取自可靠声明，不能根据默认值推断完整选项集合。

例如某版本 `org.deepin.dtk.preference.json` 的 colorMode 虽为字符串，但 visibility 为 private，应排除；defaultColorMode 是另一个项，不能未经用户选择就替代它。

这些规则来自 DConfig 元数据及 DTK 的 DConfigFile/DStandardPaths 机制；以目标机版本为准。技能部署无需作者机器上的源码路径。
