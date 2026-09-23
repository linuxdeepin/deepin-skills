# dde-polkit-agent 命令参考

DDE 的 PolicyKit 认证代理，负责在用户执行需要特权的操作时弹出认证对话框。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-polkit-agent` |
| 安装路径 | `/usr/lib/polkit-1-dde/dde-polkit-agent` |
| DDE 角色 | PolicyKit 图形化认证代理 |

## 用途

DDE 的 PolicyKit 认证代理，负责在用户执行需要特权的操作时弹出认证对话框。它监听 polkit 的认证请求，通过图形界面收集用户密码或指纹认证信息，是 DDE 权限管理的前端组件。该程序在用户会话启动时自动运行，由 DBus 激活。

## 用例

查看版本信息：

```bash
dde-polkit-agent --version
```

手动启动认证代理（通常由会话自动启动，无需手动运行）：

```bash
/usr/lib/polkit-1-dde/dde-polkit-agent
```
