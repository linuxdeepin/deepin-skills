# CLI 值处理、类型与验证

## 值操作的入口检查

读取当前值或有效默认值，以及修改或恢复前，执行运行时检查。仅列出或匹配本地元数据时无需这些条件；结果须注明目录来源、覆盖范围及运行时状态未验证。值操作的检查失败后，可继续完成用户需要的纯元数据候选，但不得读取或写入值。

1. `command -v dde-dconfig` 确认工具存在。
2. 当前用户的 `DBUS_SESSION_BUS_ADDRESS` 已设置，且该地址上的总线可达；不能借用其他用户的地址、凭空填地址或创建临时总线绕过检查。总线可达性不单靠 `systemctl --user show-environment` 判断。
3. DConfig 服务进程正在运行；常见可执行文件为 `dde-dconfig-daemon`。按本机服务定义核实进程路径、身份及服务归属，避免把其他用户或无关进程当成目标实例；不启动、重启服务或等待自动激活来绕过此约束。

只读检查示例，按顺序执行，任一步不满足立即停止后续值操作：

```bash
command -v dde-dconfig >/dev/null || exit 1
test -n "${DBUS_SESSION_BUS_ADDRESS:-}" || exit 1
# 检查所给地址上的总线是否可达；不调用 DConfig D-Bus 接口。
dbus-send --bus="$DBUS_SESSION_BUS_ADDRESS" --type=method_call --print-reply --reply-timeout=2000 \
  --dest=org.freedesktop.DBus /org/freedesktop/DBus \
  org.freedesktop.DBus.ListNames >/dev/null || exit 1
# 按本机服务定义检查目标实例的实际可执行文件、UID 及服务归属。
# 不能只用不限定 UID 的 pgrep -f 匹配进程名。
```

可读取本机 `dde-dconfig-daemon.service` 的 `User`、`ExecStart`，再用 `systemctl show dde-dconfig-daemon.service -p ActiveState -p MainPID` 和 `/proc/<MainPID>/exe`、进程 UID 核实正在运行的目标实例。该服务可能是系统服务并以专用用户运行，不要求进程 UID 等于当前操作用户。服务安装位置或管理机制不同时，依据本机定义采用等价的只读检查；不能验证则报告前提未满足，不直接试写。会话检查不意味着将 DConfig 改为会话总线接口。

以上检查通过后，在值操作入口读取 `dde-dconfig --help` 并用 `id -u` 记录当前用户；确认 get 可用，修改请求还要确认 set，恢复请求确认 reset。必需命令不支持则停止值操作。帮助只证明 CLI 支持相应操作，不证明具体 key 可读写；环境通过后先选定目标，再以 get 验证读取，写能力仅用用户授权的实际 set/reset 验证，不对未知项试写或临时 reset。环境可用不保证特定配置能获取：`get value handler error`、`not create value handler`、fallback 等均作为失败处理，停止该目标及批量后续调用。此错误不能单独证明 appId 非法；先报告环境和资源解析问题，不循环尝试猜测的 appId/resource/subpath 组合。

缺少任一前提时停止值请求；报告失败步骤和错误原因，不列只读检查命令，后续值步骤标为未执行。允许继续本地元数据检索并明确其局限。使用当前用户，不传其他 UID，不使用 sudo/su，不自动安装、不直接调用 DConfig D-Bus、不改服务环境或工作目录前缀。

## X11/Wayland 环境确认

需要选定特定配置或执行值操作时，识别目标用户的图形会话，再选择对应的配置。先读取当前会话的 `XDG_SESSION_TYPE`；可结合当前用户已确认 session ID 的 `loginctl show-session "$XDG_SESSION_ID" -p Type -p User -p Active` 交叉核实。只有 session ID 确实属于目标用户和会话时才使用，不猜测会话编号。纯元数据列表可同时展示有依据的不同会话候选，标明适用性未确认。

`DISPLAY` 存在不能单独证明是 X11，Wayland 会话可能同时运行 XWayland；`WAYLAND_DISPLAY` 仅作为补充线索，不能在环境变量冲突时据此猜测。SSH、TTY、多图形会话、缺失变量或会话信息相互矛盾时，让用户选择目标 X11/Wayland 会话，不自动选一个“活跃”会话代替目标。

会话类型无法确认时暂停配置选择和修改。可向用户说明两种环境，并在基础运行条件已通过的前提下列出有依据的候选供选择，但不能声称已确定目标。确认环境后还需从配置描述、应用实际后端或可靠安装资料确认候选适用性，不只凭文件名猜测；用户指定环境与检测结果冲突时先澄清。环境无关的配置也不能伪称经过环境验证。

## 默认值的获取

实际值和有效默认值以 CLI 返回为准，不将文件 value 或自行合并 override 的结果作为配置值输出。`isDefaultValue` 是布尔状态，不是默认值本身：

- 相同身份下 get 成功且 isDefaultValue 为 true，读到的值可标为当前有效默认值；期间如有并发变化则重新核实。
- isDefaultValue 为 false 时，当前值不能标为默认值。本机 CLI 若有经过帮助核实的默认值查询能力可使用；没有则报告“有效默认值未取得”。不能编造 `-m defaultValue`。
- 不为查询默认值临时 reset 再恢复；只有用户授权恢复默认时执行 reset，之后通过 get 和默认状态验证。

## 值读写

resource 必须对应存在的 JSON；app 和 subpath 来自已确定的调用上下文，可以动态构造，不要求有同名目录。以下变量必须绑定用户选定的目标；示例不是可直接对生产配置执行的任务：

```bash
app='实际appId或空字符串'
resource='实际resourceId，不含.json'
subpath=''
key='实际key'
dde-dconfig get -a "$app" -r "$resource" -s "$subpath" -k "$key"
dde-dconfig get -a "$app" -r "$resource" -s "$subpath" -k "$key" -m isDefaultValue
```

空 appId 必须实际赋值 `app=''`；非空子路径如 `/child`。每次值读取都指定 key，不能用无 key 的 get 枚举配置。name、description、permissions、visibility、flags、key 列表全部来自文件，不用 CLI 查询。

```bash
# 按已核实的声明类型和语义选用一种写入：
dde-dconfig set -a "$app" -r "$resource" -s "$subpath" -k "$key" -v false
dde-dconfig set -a "$app" -r "$resource" -s "$subpath" -k "$key" -v 'color'
dde-dconfig set -a "$app" -r "$resource" -s "$subpath" -k "$key" -v 2
dde-dconfig set -a "$app" -r "$resource" -s "$subpath" -k "$key" -v '["a","b"]'
# 恢复所选项的有效默认状态：
dde-dconfig reset -a "$app" -r "$resource" -s "$subpath" -k "$key"
```

所有参数作为独立参数传入；shell 单引号内的用户文本若含单引号需正确转义，优先参数数组或工具的结构化参数。不要使用 eval，也不要把 JSON.stringify 的输出当 shell 转义。

## 类型与 CLI 限制

声明类型决定目标表达，当前值用于校验与恢复，不依靠显示文本猜声明类型。字符串 `"0"` 与数字 `0`、字符串 `"false"` 与布尔 false 不等价；枚举映射以元数据描述为依据。

某些 CLI 版本根据旧值转换 bool/double，其他输入尝试 JSON 容器解析。shell 引号只是保证参数完整，不能强制 CLI 类型：`-v '[1,2]'` 在字符串项上也可能被解析为数组。看起来像 JSON 的字符串、精确数字或特殊容器只有确认本机 CLI 能无损表达时才写入，否则说明限制，不尝试加上会改变内容的引号、不直接调用其他接口。

CLI get 输出可能带展示引号，不保证是合法 JSON。不要把展示引号写入原字符串，也不要仅靠格式差异判断真实值变化。元数据与当前值明显不一致或输出不可可靠解析时停止写入。不能声称 CLI 已验证其未暴露的精确类型。

## 修改与恢复闭环

1. 重查选定元数据、有效权限、类型和已知范围。明确用户意图，记录旧值及 isDefaultValue；任一必要读取失败则不写入。原值不可无损恢复时说明具体问题。
2. 对已授权目标执行一次 set 或单 key reset。Global 项允许修改，注明共享影响；权限错误直接报告，不尝试 root 或其他用户。
3. 检查 stderr 和退出状态，随后用相同身份 get 回读；reset 还查询 isDefaultValue。部分版本写入错误仅输出 warning 而退出码为零，不能仅看退出码。
4. 回读不一致或失败时报告失败/未验证，不盲目重写。如果已知原默认状态为 true，恢复方式是单 key reset，否则按原声明类型 set 回旧值；恢复本身需要用户要求或预先约定。
5. 批量值操作串行；写入中途失败停止，逐项列出状态，不承诺原子事务。全部只读值查询也不高并发，出现服务错误停止并报告未完成范围。

出现 `fallback to local directories` 或类似提示时，不把读取当作服务当前值，不继续写入，不将本地回退当作成功。服务状态在调用过程中变化时，报告已发生操作及验证限制，不能保证 CLI 内部一定没有副作用。

reset 恢复的是有效默认状态，可能包含系统 override；不要把元数据的 value set 回去冒充 reset。配置值已更新不证明应用已采用；描述注明需要重启时转述，不自动重启。

## 命令报告

最终回复必须逐条输出实际执行的完整修改命令代码块，不可只报告值变化或引用日志。即 `dde-dconfig set`、`dde-dconfig reset`，包括执行失败的修改尝试。展示实际 appId/resource/subpath/key/value 和必要赋值，附成功、失败或未验证状态。环境检查、文件检索、get、isDefaultValue 和回读等只读操作仅概述结果或错误原因，不列命令。没有执行修改时无需“已执行命令”清单。恢复参考另行标注未执行；模拟修改标注模拟，不计入实际执行记录。

回复前对照实际调用记录逐条检查：所有已执行 set/reset（含失败、回读未验证及批量部分成功的尝试）均已完整展示，附结果状态。只读命令仍不输出。
