# org.deepin.dde.Polkit1.AuthAgent 接口参考

## 接口信息

该接口在 **Session 总线**上注册，提供 polkit 认证代理窗口 ID 设置能力，供外部应用调用以关联认证窗口。

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Polkit1.AuthAgent` |
| Object path | `/com/deepin/dde/Polkit1/AuthAgent` |
| Interface | `org.deepin.dde.Polkit1.AuthAgent` |
| Bus | Session |

## 方法

### setWIdForAction

为指定 polkit 动作设置窗口 ID。

- **功能**：为指定的 polkit action 设置关联窗口 ID，使认证对话框作为该窗口的子窗口模态显示。
- **触发条件**：在发起 polkit 认证请求前由调用方主动调用。
- **使用场景**：应用程序需要提权操作时，将自身窗口 ID 传入，使认证对话框模态显示在该应用窗口上。
- **输入参数**：
  - `action_id`（string, 类型 `s`）：polkit 动作标识符（如 `org.freedesktop.policykit.exec`）
  - `window_id`（uint64, 类型 `t`）：X11 窗口 ID
- **返回值**：无

## 示例

```bash
gdbus call --session \
  --dest org.deepin.dde.Polkit1.AuthAgent \
  --object-path /com/deepin/dde/Polkit1/AuthAgent \
  --method org.deepin.dde.Polkit1.AuthAgent.setWIdForAction "org.example.action" 12345
```

