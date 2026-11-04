# dci 命令参考

DCI 文件打包/解包工具，支持创建、导出和树形查看 DCI 文件。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DCore/bin/dci` |
| DDE 角色 | 开发辅助工具，用于 DCI 图标文件的打包、解包和查看 |

## 用途

DCI 文件打包/解包工具。如果按照正确的 DCI 目录规范创建了图标目录，可以使用此工具方便地制作 DCI 图标文件。支持三种操作模式：将目录打包为 DCI 文件（`--create`）、将 DCI 文件导出为目录（`--export`）、以树形结构查看 DCI 文件内容（`--tree`）。该工具适用于 DCI 图标资源的开发、调试和批量管理。

## 用法

`dci [options] [sources...]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `--create <targetDir>` | 将源目录打包为 DCI 文件，输出到目标目录 | 是 |
| `--export <targetDir>` | 将 DCI 文件导出为目录，输出到目标目录 | 是 |
| `--tree <dciFile>` | 以树形结构查看 DCI 文件内容 | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `sources` | 源目录路径（用于 `--create`）或 DCI 文件路径（用于 `--export`），支持多个 |

## 使用示例

```bash
# 将图标目录打包为 DCI 文件
/usr/libexec/dtk6/DCore/bin/dci --create ~/Desktop ~/Desktop/action_add

# 将 DCI 文件导出为目录
/usr/libexec/dtk6/DCore/bin/dci --export ~/Desktop ~/Desktop/action_add.dci

# 以树形结构查看 DCI 文件内容
/usr/libexec/dtk6/DCore/bin/dci --tree ~/Desktop/action_add.dci

# 查看帮助信息
/usr/libexec/dtk6/DCore/bin/dci --help
```
