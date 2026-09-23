# dci-icon-theme 命令参考

DCI 图标主题构建工具，用于将普通的图标目录结构转换为 DCI 图标主题文件。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DGui/bin/dci-icon-theme` |
| DDE 角色 | 开发调试工具，用于 DCI 图标主题构建和打包 |

## 用途

DCI 图标主题构建工具，用于将普通的图标目录结构转换为 DCI 图标主题文件。它支持通配符匹配图标文件、指定输出目录、处理符号链接关系、自动生成暗色主题的符号链接。还支持通过缩放质量参数控制图标在不同分辨率下的渲染质量。该工具是 DTK 主题开发和打包流程中的关键工具，供主题设计者和开发者使用。

## 用法

`dci-icon-theme [options] <source>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `--version` | 显示版本信息 | 否 |
| `-m, --match <wildcard>` | 图标文件匹配通配符规则 | 是 |
| `-o, --output <directory>` | 保存 .dci 文件的目标目录 | 是 |
| `-s, --symlink <csv file>` | 符号链接 CSV 文件 | 是 |
| `--fix-dark-theme` | 从亮色主题为暗色主题创建符号链接 | 否 |
| `-O, --scale-quality <scale quality>` | 缩放图标质量（如 `2=98:3=95`） | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `source` | 源目录 |

## 使用示例

```bash
# 将图标目录转换为 DCI 主题，输出到指定目录
dci-icon-theme -o /tmp/dci-output/ /path/to/icon-source/

# 使用通配符匹配特定图标文件
dci-icon-theme -m "*.png" -o /tmp/dci-output/ /path/to/icon-source/

# 指定符号链接 CSV 文件
dci-icon-theme -s symlinks.csv -o /tmp/dci-output/ /path/to/icon-source/

# 自动为暗色主题创建符号链接
dci-icon-theme --fix-dark-theme -o /tmp/dci-output/ /path/to/icon-source/

# 指定缩放质量（2x 和 3x 分辨率的质量参数）
dci-icon-theme -O "2=98:3=95" -o /tmp/dci-output/ /path/to/icon-source/
```
