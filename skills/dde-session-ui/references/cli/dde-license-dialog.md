# dde-license-dialog 命令参考

DDE 许可证对话框工具，用于展示软件许可证内容并获取用户同意。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-session-ui` |
| 安装路径 | `/usr/bin/dde-license-dialog` |
| DDE 角色 | 系统调用的辅助工具，许可证确认流程中自动弹出 |

## 用途

DDE 许可证对话框工具，用于展示软件许可证内容并获取用户同意。它支持中英文双语显示许可证标题、内容和允许复选项，可选择主题风格（亮色/暗色/自动跟随系统），支持自定义标题栏图标。该工具通常在系统首次启动、安装新软件或更新许可证时由系统自动调用，展示许可证条款并由用户确认。对话框底部可选择性显示或隐藏。

## 用法

`dde-license-dialog [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-t, --title <TitleName>` | 中文标题名 | 是 |
| `-u, --english title <EnTitleName>` | 英文标题名 | 是 |
| `-c, --content <string>` | 中文内容（文档绝对路径） | 是 |
| `-a, --allow <string>` | 中文允许复选项内容 | 是 |
| `-b, --english allow <string>` | 英文允许复选项内容 | 是 |
| `-e, --english content <string>` | 英文内容（文档绝对路径） | 是 |
| `-d, --hide bottom <string>` | 设为 `yes` 时显示底部 | 是 |
| `-p, --palette <string>` | 主题：`light`/`dark`/`auto`（默认跟随系统） | 是 |
| `-i, --icon-name <string>` | 自定义标题栏图标名 | 是 |

> 注：`--english title`、`--english allow`、`--english content`、`--hide bottom` 的长选项名使用空格而非连字符，此处按实际命令行定义记录。

## 使用示例

```bash
# 显示中文许可证对话框
dde-license-dialog -t "最终用户许可协议" -c /usr/share/licenses/eula-zh.txt

# 显示中英文双语许可证对话框
dde-license-dialog -t "最终用户许可协议" -u "End User License Agreement" -c /usr/share/licenses/eula-zh.txt -e /usr/share/licenses/eula-en.txt

# 带允许复选项的许可证对话框（用户需勾选才能继续）
dde-license-dialog -t "隐私协议" -c /usr/share/licenses/privacy-zh.txt -a "我已阅读并同意隐私协议"

# 中英文双语带允许复选项
dde-license-dialog -t "隐私协议" -u "Privacy Policy" -c /usr/share/licenses/privacy-zh.txt -e /usr/share/licenses/privacy-en.txt -a "我已阅读并同意" -b "I have read and agree"

# 指定暗色主题显示
dde-license-dialog -t "许可协议" -c /usr/share/licenses/eula-zh.txt -p dark

# 显示底部按钮区域
dde-license-dialog -t "许可协议" -c /usr/share/licenses/eula-zh.txt -d yes

# 自定义标题栏图标
dde-license-dialog -t "许可协议" -c /usr/share/licenses/eula-zh.txt -i preferences-system
```

> 注意：`dde-license-dialog` 是图形对话框工具，需要图形显示环境（X11/Wayland），在无 DISPLAY 的终端中运行会失败。
