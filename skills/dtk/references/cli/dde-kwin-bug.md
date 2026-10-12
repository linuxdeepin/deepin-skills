# dde-kwin-bug 命令参考

DDE KWin 调试工具，用于输出 KWin 窗口管理器的调试信息。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DGui/bin/dde-kwin-bug` |
| DDE 角色 | KWin 窗口管理器的调试辅助工具 |

## 用途

DDE KWin 调试工具，用于输出 KWin 窗口管理器的调试信息。它是开发调试用途的辅助工具，帮助开发者诊断窗口管理相关问题。

## 用法

`dde-kwin-bug [options] [applications...]`

## 参数

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-k` | 测试结束后自动终止应用 | — |
| `-L` | 禁用应用输出（重定向到 /dev/null） | — |
| `-a` | 监视所有窗口 | — |
| `--format <format>` | 日志格式，支持 `%p`（PID）、`%t`（启动时间 ms）、`%n`（应用名） | — |
| `-no--cache` | 禁用缓存 | — |
| `--r <count>` | 重复次数 | — |
| `--ci <ms>` | 检查间隔 | 100ms |
| `--cpt <ms>` | 窗口 ping 回复时间 | 50ms |
| `--cvc <count>` | 检查有效次数 | 10 |
| `--cdc <count>` | 检查 damage 次数 | 20 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `applications` | 待监视的应用名列表 |

## 使用示例

```bash
# 监视指定应用的 KWin 窗口调试信息
/usr/libexec/dtk6/DGui/bin/dde-kwin-bug dde-desktop

# 监视多个应用并使用自定义日志格式
/usr/libexec/dtk6/DGui/bin/dde-kwin-bug --format "[%p] %n: %t ms" dde-desktop dde-dock

# 监视所有窗口，禁用应用输出
/usr/libexec/dtk6/DGui/bin/dde-kwin-bug -a -L

# 设置检查间隔为 200ms，重复 3 次
/usr/libexec/dtk6/DGui/bin/dde-kwin-bug --ci 200 --r 3 dde-desktop
```
