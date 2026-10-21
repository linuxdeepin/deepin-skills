# dde-wm-chooser 命令参考

显示窗口模式选择界面，将选择写入调用方指定的 JSON 配置文件，不直接替换当前窗口管理器。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session-ui` |
| 安装路径 | `/usr/bin/dde-wm-chooser` |
| DDE 角色 | 窗口模式选择及配置保存工具 |

## 用法与参数

`dde-wm-chooser -c CONFIG_PATH`

| 选项 | 说明 |
|------|------|
| `-h, --help` | 显示命令行帮助 |
| `-c, --config <ConfigPath>` | 选择结果的输出文件路径，不是可选窗口管理器列表的输入文件 |

未指定 `-c` 时直接退出，不显示选择界面。桌面版本显示预设模式：选择高效果模式写入 `last_wm=deepin-wm`，选择普通模式写入 `last_wm=deepin-metacity`，并保存 `allow_switch=true`。服务器版本直接保存普通模式。

写入文件不等于当前会话立即切换；是否在后续启动中使用这些值，由对应会话启动配置决定。此工具不提供任意 kwin/deepin-wm 候选列表加载，也不能据此替换 Wayland 合成器。

风险警示：

- 选择后覆盖指定文件的内容；应使用预期的、当前用户可写的配置目标，不要把现有系统文件当作输出路径。

## 使用示例

需要图形环境。下面示例明确写入用户文档目录中的示例文件，是否采用其结果由调用方决定：

```bash
# 先准备调用方指定的输出目录，再显示选择界面
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/deepin-wm-chooser-example"
dde-wm-chooser -c "${XDG_CONFIG_HOME:-$HOME/.config}/deepin-wm-chooser-example/selection.json"
```
