# ipwatchd 命令参考

IP 地址监视守护进程（upstream 开源项目），用于监视网络接口的 IP 地址变化。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-services`（集成 upstream ipwatchd） |
| 安装路径 | `/usr/sbin/ipwatchd` |
| DDE 角色 | 系统调用的底层网络辅助工具 |

## 用途

IP 地址监视守护进程（upstream 开源项目），用于监视网络接口的 IP 地址变化。当网络接口的 IP 地址发生添加、删除或变更时，ipwatchd 可以执行相应的通知或脚本操作。在 DDE 中，该工具作为网络管理的底层辅助组件，帮助网络模块及时感知 IP 变化并做出响应。支持配置文件指定监视规则，提供调试和测试模式便于开发排查。

## 用法

`ipwatchd [options]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-c, --config <config_file>` | 配置文件路径（必填） | 是 |
| `-d, --debug` | 调试模式 | 否 |
| `-t, --test` | 测试模式 | 否 |
| `-h, --help` | 显示帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |

## 使用示例

```bash
# 使用默认配置文件启动 IP 监视守护进程
ipwatchd -c /etc/ipwatchd.conf

# 以调试模式启动（输出详细调试信息）
ipwatchd -c /etc/ipwatchd.conf -d

# 以测试模式启动（仅测试配置是否正确，不实际运行）
ipwatchd -c /etc/ipwatchd.conf -t

# 查看版本信息
ipwatchd -v
```
