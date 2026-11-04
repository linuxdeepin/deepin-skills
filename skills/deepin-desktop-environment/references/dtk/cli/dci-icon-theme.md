# dci-icon-theme 命令参考

DCI 图标主题生成工具，从普通图标（PNG/SVG）批量生成 DCI 图标文件。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DGui/bin/dci-icon-theme` |
| DDE 角色 | 开发辅助工具，用于从普通图标批量生成 DCI 图标文件 |

## 用途

DCI 图标主题生成工具。扫描源目录及其子目录中的普通图标文件（如 PNG、SVG），按照 DCI 目录规范将它们打包为 DCI 格式图标文件。支持通过通配符筛选图标文件、指定输出目录、生成符号链接映射文件、为暗色主题创建链接以及设置缩放图片质量。适用于 DCI 图标主题的批量构建和转换开发。

## 用法

`dci-icon-theme [options] <source>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `-m, --match <wildcard>` | 指定通配符规则筛选图标文件 | 是 |
| `-o, --output <directory>` | 指定 DCI 文件输出的目录 | 是 |
| `-s, --symlink <csv-file>` | 指定 CSV 文件用于创建输出图标的符号链接 | 是 |
| `--fix-dark-theme` | 为暗色主题文件创建从亮色主题的符号链接 | 否 |
| `-O, --scale-quality <quality>` | 设置 DCI 缩放图标的图片质量，格式为 `<scale>=<quality>`，例如 `2=98:3=95`，质量值范围为 0-100 或 -1 | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `source` | 源目录路径，将搜索该目录及其子目录中符合规则的图标文件 |

## 使用示例

```bash
# 将图标目录转换为 DCI 文件并输出到指定目录
/usr/libexec/dtk6/DGui/bin/dci-icon-theme /usr/share/icons/hicolor/256x256/apps -o ~/Desktop/hicolor

# 使用通配符筛选并指定缩放质量
/usr/libexec/dtk6/DGui/bin/dci-icon-theme -m "*.png" /usr/share/icons/hicolor/256x256/apps -o ~/Desktop/hicolor -O 3=95

# 为暗色主题创建符号链接
/usr/libexec/dtk6/DGui/bin/dci-icon-theme --fix-dark-theme /path/to/icons -o /path/to/output

# 使用 CSV 文件创建符号链接
/usr/libexec/dtk6/DGui/bin/dci-icon-theme /path/to/icons -o /path/to/output -s symlinks.csv -O 2=98:3=95

# 查看帮助信息
/usr/libexec/dtk6/DGui/bin/dci-icon-theme --help
```
