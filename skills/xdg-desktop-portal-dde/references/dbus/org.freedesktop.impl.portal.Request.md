# org.freedesktop.impl.portal.Request 接口参考

该接口提供标准 Portal 请求的生命周期管理能力，每个 Portal 请求会创建一个独立的 Request 对象，用于关闭请求和释放资源。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | 动态对象路径，由 Portal 后端在创建请求时生成 |
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
  --object-path /org/freedesktop/portal/desktop/request/dde/1 \
  --method org.freedesktop.impl.portal.Request.Close
```
