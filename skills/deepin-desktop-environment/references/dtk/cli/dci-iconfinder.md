# dci-iconfinder 命令参考

DCI 图标查找工具，在图标主题中查找指定图标的 DCI 文件路径。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DGui/bin/dci-iconfinder` |
| DDE 角色 | 开发辅助工具，用于在图标主题中查找 DCI 图标文件路径 |

## 用途

DCI 图标查找工具。根据图标名称在指定的图标主题中查找对应的 DCI 图标文件路径。如果不指定主题名称，则使用当前系统默认图标主题。适用于 DCI 图标资源的查找和调试，帮助开发者确认图标文件是否正确安装和定位。

## 用法

`dci-iconfinder [options] <iconnames...>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `-t, --theme <theme name>` | 指定要查找的图标主题名称 | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `iconnames` | 要查找的图标名称列表 |

## 使用示例

```bash
# 使用默认图标主题查找图标
/usr/libexec/dtk6/DGui/bin/dci-iconfinder edit-cut

# 指定图标主题查找图标
/usr/libexec/dtk6/DGui/bin/dci-iconfinder -t bloom edit-cut

# 查找多个图标
/usr/libexec/dtk6/DGui/bin/dci-iconfinder -t bloom edit-cut edit-copy edit-paste

# 查看帮助信息
/usr/libexec/dtk6/DGui/bin/dci-iconfinder --help
```
