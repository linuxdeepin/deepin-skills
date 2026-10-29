# org.deepin.dde.Polkit1.AuthAgent 接口参考

认证代理的窗口关联接口。调用方在发起 Polkit 授权前，把待授权动作与当前应用的顶层窗口标识关联，认证代理据此确定对话框的父窗口。该接口只记录窗口关联信息，不授予权限，也不代替用户完成认证。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Polkit1.AuthAgent` |
| Object path | `/com/deepin/dde/Polkit1/AuthAgent` |
| Interface | `org.deepin.dde.Polkit1.AuthAgent` |
| Bus | Session |

```bash
busctl --user introspect org.deepin.dde.Polkit1.AuthAgent /com/deepin/dde/Polkit1/AuthAgent
```

按实际输出报告接口成员；不要为了探查而调用 `setWIdForAction`。空节点不等于服务未运行，应区分服务、对象与接口三个层级。

`ServiceUnknown` 表示当前 Session 总线服务不可用；`UnknownObject` 或空节点需核对对象路径；`UnknownInterface` 需核对对象接口及版本。

这不是 System 总线的 `Authenticate1` 认证框架，也不是旧 `org.freedesktop.PolicyKit1.AuthenticationAgent` 接口；以上错误均不能证明某个 Polkit 动作不存在。

## 方法

### setWIdForAction

为指定动作设置窗口标识。

- **功能**：把后续 Polkit 授权对话框关联到调用方提供的顶层窗口，不改变动作的授权结果。
- **输入参数**：
  - `actionId`（string, 类型 `s`）：待授权动作 ID，例如 `org.deepin.dde.skillstest`
  - `wid`（uint64, 类型 `t`）：顶层窗口标识；`0` 也会被接受，具体语义由代理实现决定
- **返回值**：无
- **触发条件**：调用方准备发起需要图形认证的动作时调用。
- **使用场景**：让认证对话框以调用方窗口为父窗口，避免对话框出现在无关窗口上。

重复使用相同的 `actionId` 和 `wid` 调用不会报错，可视为幂等操作。

```bash
gdbus call --session \
  --dest org.deepin.dde.Polkit1.AuthAgent \
  --object-path /com/deepin/dde/Polkit1/AuthAgent \
  --method org.deepin.dde.Polkit1.AuthAgent.setWIdForAction \
  "org.deepin.dde.skillstest" 0
```

## 边界

- 认证代理未运行或服务未注册时，可能返回 `org.freedesktop.DBus.Error.ServiceUnknown`；服务存在但对象或接口不可用时可能返回 `UnknownObject` 或 `UnknownInterface`。不要据此判断动作不存在。
- `wid` 为 `0` 时调用仍可成功，但不代表已经完成具体窗口关联。
- 不要把本接口用于代替授权、绕过 Polkit 或代填密码。
