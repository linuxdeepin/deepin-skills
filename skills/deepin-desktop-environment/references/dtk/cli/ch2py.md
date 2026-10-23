# ch2py 命令参考

中文转拼音工具，将输入的中文字符串转换为拼音。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DCore/bin/ch2py` |
| DDE 角色 | 开发辅助工具，用于中文转拼音 |

## 用途

中文转拼音工具，将输入的中文字符串转换为拼音。支持多种声调风格（带声调、不带声调、数字声调），也支持仅提取拼音首字母。该工具基于 DTK 内置的拼音数据，适用于中文搜索和排序场景的辅助开发。

## 用法

`ch2py [options] <words>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-s, --tonestyle <style>` | 声调风格：`tones`（带声调，默认）、`notones`（不带声调）、`numtones`（数字声调） | 是 |
| `-l, --letters` | 仅输出拼音首字母 | 否 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `words` | 待转换的中文字符串 |

## 使用示例

```bash
# 将中文转换为带声调的拼音（默认）
/usr/libexec/dtk6/DCore/bin/ch2py 你好世界

# 转换为不带声调的拼音
/usr/libexec/dtk6/DCore/bin/ch2py --tonestyle notones 你好世界

# 转换为数字声调的拼音
/usr/libexec/dtk6/DCore/bin/ch2py -s numtones 你好世界

# 仅输出拼音首字母
/usr/libexec/dtk6/DCore/bin/ch2py --letters 你好世界
```
