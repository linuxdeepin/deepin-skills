# adjust-grub-theme 命令参考

GRUB 主题调整工具，用于根据屏幕分辨率和语言环境自动调整 GRUB 启动菜单的主题显示。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-api` |
| 安装路径 | `/usr/lib/deepin-api/adjust-grub-theme` |
| DDE 角色 | 系统调用的辅助工具，在主题或分辨率变更时自动运行 |

## 用途

GRUB 主题调整工具，用于根据屏幕分辨率和语言环境自动调整 GRUB 启动菜单的主题显示。它会从主题输入目录读取原始 GRUB 主题文件，根据指定的屏幕宽高和语言参数进行适配处理，将结果输出到主题输出目录（默认 `/boot/grub/themes/`）。还支持设置背景图片和调整终端字体。该工具通常在系统安装、分辨率变更或主题更新时由系统自动调用，确保 GRUB 启动界面在不同硬件上正确显示。使用 Go flag 风格参数。

## 用法

`/usr/lib/deepin-api/adjust-grub-theme [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-width <int>` | 屏幕宽度（默认 0） | 是 |
| `-height <int>` | 屏幕高度（默认 0） | 是 |
| `-theme-input <string>` | 主题输入目录（默认 `/usr/share/dde-api/grub-themes/`） | 是 |
| `-theme-output <string>` | 主题输出目录（默认 `/boot/grub/themes/`） | 是 |
| `-lang <string>` | 语言（默认空） | 是 |
| `-version` | 显示版本信息 | 否 |
| `-set-background <string>` | 设置背景（隐藏选项） | 是 |
| `-log-sys` | 记录到 syslog（隐藏选项） | 否 |
| `-tf-size <int>` | 终端字体大小（默认 -1） | 是 |
| `-tf-name <string>` | 终端字体名称（默认 `Unifont:style=Medium`） | 是 |
| `-fallback-only` | 仅使用后备 | 否 |

## 使用示例

```bash
# 根据当前屏幕分辨率 1920x1080 调整 GRUB 主题
/usr/lib/deepin-api/adjust-grub-theme -width 1920 -height 1080

# 指定屏幕分辨率和语言环境
/usr/lib/deepin-api/adjust-grub-theme -width 1920 -height 1080 -lang zh_CN

# 使用自定义主题输入和输出目录
/usr/lib/deepin-api/adjust-grub-theme -width 2560 -height 1440 -theme-input /opt/my-grub-themes/ -theme-output /tmp/grub-output/

# 设置 GRUB 背景图片（隐藏选项）
/usr/lib/deepin-api/adjust-grub-theme -width 1920 -height 1080 -set-background /usr/share/backgrounds/grub-bg.png

# 调整终端字体大小和名称
/usr/lib/deepin-api/adjust-grub-theme -width 1920 -height 1080 -tf-size 16 -tf-name "DejaVu Sans Mono"

# 仅使用后备主题
/usr/lib/deepin-api/adjust-grub-theme -width 1920 -height 1080 -fallback-only

# 记录到 syslog（隐藏选项，用于系统日志记录）
/usr/lib/deepin-api/adjust-grub-theme -width 1920 -height 1080 -log-sys

# 查看版本信息
/usr/lib/deepin-api/adjust-grub-theme -version
```
