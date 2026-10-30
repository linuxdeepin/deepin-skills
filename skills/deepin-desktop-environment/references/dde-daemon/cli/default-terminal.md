# default-terminal 命令参考

启动当前用户配置的默认终端。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-daemon` |
| 安装路径 | `/usr/lib/deepin-daemon/default-terminal` |
| DDE 角色 | 默认终端启动工具 |

## 用途

读取当前用户配置的默认终端并启动；传入参数时将参数转交给终端程序。无参数时通过应用管理器启动默认终端，无法启动时尝试可用的后备终端。该工具不修改默认终端关联。

## 使用示例

在当前用户的 DDE 图形会话中运行：

```bash
/usr/lib/deepin-daemon/default-terminal
```

向终端转交执行参数（取决于已配置终端对 `-e` 的支持）：

```bash
/usr/lib/deepin-daemon/default-terminal -e /usr/bin/printf "hello\n"
```
