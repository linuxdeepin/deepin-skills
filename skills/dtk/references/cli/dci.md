# dci 命令参考

DCI 文件打包/解包工具，用于将符合 DCI 目录规范的图标目录打包为 `.dci` 文件，或将 `.dci` 文件导出为目录结构，还支持以树形结构查看 DCI 文件内容。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DCore/bin/dci` |
| DDE 角色 | 开发调试工具，用于 DCI 图标资源打包、解包和查看 |

## 用途

DCI 文件打包/解包工具，用于将符合 DCI 目录规范的图标目录打包为 `.dci` 文件，或将 `.dci` 文件导出为目录结构，还支持以树形结构查看 DCI 文件内容。DCI（Deepin Custom Image）是 DTK 框架自研的图片格式，支持多分辨率、状态切换和动画效果，广泛用于 DDE 图标和 UI 图片资源。该工具是 DTK 开发工具链的核心工具之一。

## 用法

`dci [options] [sources...]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `--create <targetDirectory>` | 将目录打包为 DCI 文件，目标路径为输出目录 | 是 |
| `--export <targetDirectory>` | 将 DCI 文件导出为目录，目标路径为输出目录 | 是 |
| `--tree <targetDciFile>` | 以树形结构查看 DCI 文件内容 | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `sources` | `--create` 时为源目录列表；`--export` 时为源 DCI 文件列表 |

## 使用示例

```bash
# 将图标目录打包为 DCI 文件（输出到 ~/Desktop/ 目录下生成 action_add.dci）
dci --create ~/Desktop ~/Desktop/action_add

# 将 DCI 文件导出为目录（输出到 ~/Desktop/ 目录下生成 action_add/ 目录）
dci --export ~/Desktop ~/Desktop/action_add.dci

# 以树形结构查看 DCI 文件内容
dci --tree ~/Desktop/action_add.dci

# 查看帮助信息
dci --help
```
