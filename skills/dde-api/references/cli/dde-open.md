# dde-open 命令参考

DDE 文件/URL 打开工具，用于通过默认关联应用打开文件或 URL。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-api` |
| 安装路径 | `/usr/bin/dde-open` |
| DDE 角色 | 用户和系统均可使用的文件/URL 打开工具 |

## 用途

DDE 文件/URL 打开工具，用于通过默认关联应用打开文件或 URL。它是 DDE 中 `xdg-open` 的等价替代，根据文件类型或 URL 协议自动选择合适的应用打开。例如打开文本文件会用默认编辑器，打开 HTTP 链接会用默认浏览器，打开图片会用默认图片查看器。该工具用户可以直接使用，也常被其他程序和脚本调用来实现"打开"功能。使用 Go flag 风格参数。

## 用法

`dde-open [options] <file-or-url>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-version` | 显示版本信息 | 否 |

## 位置参数

| 参数 | 说明 |
|------|------|
| file-or-url | 文件路径或 URL（恰好 1 个参数） |

## 使用示例

```bash
# 用默认应用打开文件
dde-open /home/user/document.pdf

# 用默认浏览器打开 URL
dde-open https://www.deepin.org

# 用默认编辑器打开文本文件
dde-open /home/user/notes.txt

# 打开目录（用默认文件管理器）
dde-open /home/user/Documents

# 查看版本信息
dde-open -version
# 输出：
# 1.0
```
