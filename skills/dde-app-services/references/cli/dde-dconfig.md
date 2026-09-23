# dde-dconfig 命令参考

DDE 配置（dconfig）命令行管理工具，用于管理 DTK 提供的配置策略系统（dconfig）。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-dconfig`（属于 `dde-dconfig-daemon` 包） |
| 安装路径 | `/usr/bin/dde-dconfig` |
| DDE 角色 | 用户和开发者均可使用的配置管理命令行工具；系统脚本和运维流程中也常调用 |

## 用途

DDE 配置（dconfig）命令行管理工具，用于管理 DTK 提供的配置策略系统（dconfig）。dconfig 是 DDE 中统一的配置管理中心，允许应用通过标准化的配置描述文件声明可配置项，用户和系统可以对这些配置项进行读写操作。该工具支持列出所有可配置的应用和配置项、查询指定配置项的值和元信息、设置和重置配置项的值、监听配置变化以及启动图形化配置编辑器。典型使用场景包括：系统管理员批量调整应用配置、开发者在调试时查看和修改配置项、运维脚本中自动化配置管理。

## 用法

`dde-dconfig <subcommand> [options]`

## 子命令

| 子命令 | 说明 |
|--------|------|
| `list` | 列出可配置的应用 ID、配置 ID 及子目录 |
| `get` | 查询指定配置项的信息 |
| `set` | 设置配置项的值 |
| `reset` | 重置配置项的值，清除对应缓存值；若未指定 `-k` 则重置该配置文件的所有缓存值 |
| `watch` | 监听配置项的更改 |
| `gui` | 启动 GUI 工具（需安装 `dde-dconfig-editor`） |

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-u <uid>` | 用户 UID，对指定用户的配置项进行读写操作 | 是 |
| `-a <appid>` | 应用 ID；未设置时使用第二个位置参数 | 是 |
| `-r <resource>` | 配置 ID（配置描述文件名）；未设置时与应用 ID 相同 | 是 |
| `-s <subpath>` | 子目录，配置描述文件安装可包含子路径 | 是 |
| `-k <key>` | 配置项 Key；未设置时使用第三个位置参数 | 是 |
| `-v <value>` | 需要设置的配置项值（set 模式） | 是 |
| `-p <prefix>` | 配置策略的工作目录前缀 | 是 |
| `-m <method>` | 指定配置项字段信息，值为 `name`/`description`/`visibility`/`permissions`/`version`/`isDefaultValue` 之一（get 模式） | 是 |
| `-l <language>` | 指定语言（get 模式，需同时指定 `-m`） | 是 |

## 使用示例

```bash
# 列出所有支持配置的应用 ID
dde-dconfig list
# 输出示例（部分）：
# org.deepin.dde.appearance
# org.deepin.dde.daemon
# org.deepin.dde.dconfig
# org.deepin.dde.desktop
# org.deepin.dde.dock
# ...

# 列出指定应用的所有配置项
dde-dconfig list -a org.deepin.dde.appearance
# 输出示例（部分）：
# org.deepin.dde.appearance.application/org.deepin.dde.appearance/assets/cupertino/icons-hour.json
# org.deepin.dde.appearance.application/org.deepin.dde.appearance/assets/cupertino/icons-minute.json
# org.deepin.dde.appearance.application/org.deepin.dde.appearance/assets/cupertino/icons-second.json
# org.deepin.dde.appearance.application/org.deepin.dde.appearance.gschema
# org.deepin.dde.appearance.application/org.deepin.dde.appearance/font-clockfont-size
# org.deepin.dde.appearance.application/org.deepin.dde.appearance/gtk-theme
# org.deepin.dde.appearance.application/org.deepin.dde.appearance/icon-theme
# org.deepin.dde.appearance.application/org.deepin.dde.appearance/Font_Size
# org.deepin.dde.appearance.application/org.deepin.dde.appearance/Font_Serif
# org.deepin.dde.appearance.application/org.deepin.dde.appearance/Font_Mono
# org.deepin.dde.appearance.application/org.deepin.dde.appearance/Font_Standard
# org.deepin.dde.appearance.application/org.deepin.dde.appearance/ActiveFont
# ...

# 查询 appearance 的 Font_Size 配置值
dde-dconfig get -a org.deepin.dde.appearance -k Font_Size
# 输出：
# 10.5

# 查询配置项的名称（使用 -m 指定字段）
dde-dconfig get -a org.deepin.dde.appearance -k Font_Size -m name
# 输出：
# Font_Size

# 查询配置项的中文描述（使用 -l 指定语言）
dde-dconfig get -a org.deepin.dde.appearance -k Font_Size -m description -l zh_CN
# 输出：
# 字体大小

# 查询配置项是否为默认值
dde-dconfig get -a org.deepin.dde.appearance -k Font_Size -m isDefaultValue
# 输出：
# true

# 设置 appearance 的字体大小为 12
dde-dconfig set -a org.deepin.dde.appearance -k Font_Size -v 12

# 重置 appearance 的 Font_Size 配置项为默认值
dde-dconfig reset -a org.deepin.dde.appearance -k Font_Size

# 重置 appearance 应用所有配置项
dde-dconfig reset -a org.deepin.dde.appearance

# 监听 appearance 的配置变化（实时输出变更信息）
dde-dconfig watch -a org.deepin.dde.appearance -k Font_Size

# 对指定 UID 用户的配置进行操作（如 UID 1000）
dde-dconfig get -a org.deepin.dde.appearance -k Font_Size -u 1000
# 输出：
# 10.5

# 启动 dconfig 图形化编辑器
dde-dconfig gui

# 使用位置参数简写方式查询配置值（等价于 -a 和 -k）
dde-dconfig get org.deepin.dde.appearance Font_Size
# 输出：
# 10.5
```

> 注意：`dde-dconfig gui` 需要图形显示环境（X11/Wayland），在无 DISPLAY 的终端中运行会失败。
