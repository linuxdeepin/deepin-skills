# deepin-gui-settings 命令参考

DTK GUI 设置工具，用于读写 X11 窗口属性设置。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DGui/bin/deepin-gui-settings` |
| DDE 角色 | 开发调试工具，用于窗口属性读写和调试 |

## 用途

DTK GUI 设置工具，用于读写 X11 窗口属性设置。它可以直接操作窗口的属性（如窗口标题、图标和透明度），支持通过窗口 ID 或在屏幕上选择窗口来指定目标窗口。可以设置字符串、整数和颜色类型的属性值，也支持移除指定属性。该工具主要用于 DTK 窗口属性的调试和自定义，适用于开发者和高级用户。

## 用法

`deepin-gui-settings [options] [keys]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `--version` | 显示版本信息 | 否 |
| `-w, --window <id>` | 窗口资源 ID（默认 0） | 是 |
| `--window-leader` | 使用窗口的 leader 窗口 | 否 |
| `--select` | 在屏幕上自动选择窗口 | 否 |
| `-p, --domain <domain>` | 设置属性的域 | 是 |
| `--set` | 设置一个设置项的值 | 否 |
| `-s, --string <value>` | 设置字符串值 | 是 |
| `-i, --int <value>` | 设置整数值 | 是 |
| `-c, --color <value>` | 设置颜色值 | 是 |
| `-r, --remove <key>` | 移除一个设置项 | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `keys` | 获取设置值的 key |

## 使用示例

```bash
# 获取指定窗口（ID 0x3a00006）的某个属性值
deepin-gui-settings -w 0x3a00006 WM_NAME

# 通过鼠标在屏幕上选择窗口并获取属性
deepin-gui-settings --select WM_NAME

# 使用窗口的 leader 窗口获取属性
deepin-gui-settings --window-leader WM_NAME

# 设置字符串类型的窗口属性
deepin-gui-settings -w 0x3a00006 --set -s "My Window" WM_NAME

# 设置整数类型的窗口属性
deepin-gui-settings -w 0x3a00006 --set -i 100 _NET_WM_DESKTOP

# 设置颜色类型的窗口属性
deepin-gui-settings -w 0x3a00006 --set -c "#FF0000" background-color

# 指定属性的域
deepin-gui-settings -w 0x3a00006 -p my-domain WM_NAME

# 移除指定窗口属性
deepin-gui-settings -w 0x3a00006 -r WM_NAME
```
