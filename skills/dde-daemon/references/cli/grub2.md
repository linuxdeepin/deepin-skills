# grub2 命令参考

GRUB2 相关工具，用于 GRUB 启动菜单的图形模式检测、主题设置和系统编号查询。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-daemon` |
| 安装路径 | `/usr/lib/deepin-daemon/grub2` |
| DDE 角色 | 系统调用的辅助工具，GRUB 配置变更时自动调用 |

## 用途

GRUB2 相关工具，用于 GRUB 启动菜单的图形模式检测、主题设置和系统编号查询。在 DDE 中，该工具配合 `adjust-grub-theme` 工作，负责检测显卡支持的图形模式、处理 GRUB 主题配置以及获取当前系统在 GRUB 启动菜单中的编号（用于多系统场景）。使用 Go flag 风格参数，通常在系统安装、更新或主题变更时由系统自动调用。

## 用法

`/usr/lib/deepin-daemon/grub2 [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-debug` | 调试模式 | 否 |
| `-prepare-gfxmode-detect` | 准备图形模式检测 | 否 |
| `-setup-theme` | 设置主题（为兼容性保留，实际无操作） | 否 |
| `-os-num` | 获取系统编号 | 否 |

## 使用示例

```bash
# 获取当前系统在 GRUB 启动菜单中的编号（多系统场景）
/usr/lib/deepin-daemon/grub2 -os-num

# 准备图形模式检测（检测显卡支持的分辨率模式）
/usr/lib/deepin-daemon/grub2 -prepare-gfxmode-detect

# 以调试模式运行
/usr/lib/deepin-daemon/grub2 -debug

# 设置 GRUB 主题（为兼容性保留，实际无操作）
/usr/lib/deepin-daemon/grub2 -setup-theme
```
