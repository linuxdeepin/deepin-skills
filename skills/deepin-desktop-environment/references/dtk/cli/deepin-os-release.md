# deepin-os-release 命令参考

系统信息查询工具，用于输出 deepin/UOS 操作系统的各项信息。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DCore/bin/deepin-os-release` |
| DDE 角色 | 系统信息查询工具 |

## 用途

系统信息查询工具，用于输出 deepin/UOS 操作系统的各项信息。支持查询系统类型、版本、版本号、版权信息、产品类型、CPU 型号、内存大小、磁盘大小、发行版信息。可以一次输出所有信息，也可以指定单项查询。该工具是 DTK 系统信息模块的命令行接口。

## 用法

`deepin-os-release [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `--all` | 输出所有系统信息 | 否 |
| `--deepin-type` | 输出 deepin 类型 | 否 |
| `--deepin-version` | 输出 deepin 版本号 | 否 |
| `--deepin-edition` | 输出 deepin 版本名称 | 否 |
| `--deepin-copyright` | 输出 deepin 版权信息 | 否 |
| `--product-type` | 输出产品类型 | 否 |
| `--product-version` | 输出产品版本 | 否 |
| `--computer-name` | 输出计算机名称 | 否 |
| `--cpu-model` | 输出 CPU 型号 | 否 |
| `--installed-memory-size` | 输出已安装内存大小（GiB） | 否 |
| `--memory-size` | 输出内存大小（GiB） | 否 |
| `--disk-size` | 输出磁盘大小（GiB） | 否 |
| `--distribution-info` | 输出发行版信息 | 否 |
| `--distributer-info` | 输出发行者信息 | 否 |

## 使用示例

```bash
# 输出所有系统信息
/usr/libexec/dtk6/DCore/bin/deepin-os-release --all

# 查询 deepin 版本号
/usr/libexec/dtk6/DCore/bin/deepin-os-release --deepin-version

# 查询 CPU 型号
/usr/libexec/dtk6/DCore/bin/deepin-os-release --cpu-model

# 查询内存大小（GiB）
/usr/libexec/dtk6/DCore/bin/deepin-os-release --memory-size

# 查询产品类型和版本
/usr/libexec/dtk6/DCore/bin/deepin-os-release --product-type
/usr/libexec/dtk6/DCore/bin/deepin-os-release --product-version

# 查看帮助信息
/usr/libexec/dtk6/DCore/bin/deepin-os-release --help
```
