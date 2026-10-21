# org.deepin.dde.Polkit1.AuthAgent 历史接口说明

该接口保留 `setWIdForAction(s action, t windowId)` 的历史签名。当前方法不应用传入的 action 或窗口 ID，不提供有效的认证窗口关联功能，不用于新调用。

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Polkit1.AuthAgent` |
| Object path | `/com/deepin/dde/Polkit1/AuthAgent` |
| Interface | `org.deepin.dde.Polkit1.AuthAgent` |
| Bus | Session |

接口仍可被内省不表示窗口关联已经生效；调用成功也不授予权限，不发起认证，不保证对话框作为调用方窗口的模态子窗口显示。授权交互由实际服务的 PolicyKit 请求和认证代理处理。
