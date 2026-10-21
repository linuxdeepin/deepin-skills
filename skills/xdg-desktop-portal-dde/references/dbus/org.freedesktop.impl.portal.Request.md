# org.freedesktop.impl.portal.Request 接口参考

该接口提供标准 Portal 请求的生命周期管理能力，支持取消的交互会注册对应的动态 Request 对象，用于关闭请求和释放资源。

本文记录 Portal 后端协作接口，普通应用调用前端 `org.freedesktop.portal.Desktop` 的 `org.freedesktop.portal.*` 接口。后端示例中的应用身份与请求句柄必须来自实际前端请求，不能将演示参数用于应用权限判断。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | 使用前端传给后端的实际请求 handle |
| Interface | `org.freedesktop.impl.portal.Request` |
| Bus | Session |

### 请求方法

#### Close

关闭 Portal 请求。

- **功能**: 关闭当前 Portal 请求，释放请求占用的资源并注销对应的 D-Bus 对象。调用后请求对象将被销毁，不可再次访问。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求取消正在进行的 Portal 操作时触发。
- **使用场景**: 沙箱应用在用户取消文件选择对话框、截图操作和取色操作这些 Portal 交互时，调用此方法清理请求资源。
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path "${portal_handle:?请使用仍有效的后端请求 handle}" \
  --method org.freedesktop.impl.portal.Request.Close
```

后端请求路径来自实际交互，取消后不能继续复用。应用侧应关闭前端返回的 `org.freedesktop.portal.Request` 对象，不直接调用此后端接口；抑制请求关闭时还会释放对应会话抑制。
