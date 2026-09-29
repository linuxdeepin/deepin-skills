# dci-iconfinder 命令参考

DCI 图标查找工具，用于在已安装的 DCI 图标主题中搜索指定名称的图标文件。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DGui/bin/dci-iconfinder` |
| DDE 角色 | 开发调试工具，用于 DCI 图标资源查找和定位 |

## 用途

DCI 图标查找工具，用于在已安装的 DCI 图标主题中搜索指定名称的图标文件。它帮助开发者和主题设计者快速定位图标资源所在位置，支持指定主题名称进行搜索。在 DDE 主题开发和调试过程中，该工具可以快速验证图标是否存在、确认图标路径，是图标资源管理的辅助工具。

## 用法

`dci-iconfinder [options] <iconnames>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `--version` | 显示版本信息 | 否 |
| `-t, --theme <theme name>` | 搜索的主题名 | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `iconnames` | 待搜索的图标名（可多个） |

## 使用示例

```bash
# 在默认主题中搜索指定图标
/usr/libexec/dtk6/DGui/bin/dci-iconfinder preferences-system

# 在指定主题中搜索图标
/usr/libexec/dtk6/DGui/bin/dci-iconfinder -t bloom preferences-system

# 同时搜索多个图标
/usr/libexec/dtk6/DGui/bin/dci-iconfinder -t bloom preferences-system folder-open document-new

# 查看版本信息
/usr/libexec/dtk6/DGui/bin/dci-iconfinder --version
```
