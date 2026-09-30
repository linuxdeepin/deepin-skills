# org.deepin.dde.Welcome1 接口参考

该接口为 D-Bus 激活型服务，用于欢迎界面的进程单实例控制。服务本身不导出 D-Bus 方法，通过 D-Bus 服务激活机制启动 `dde-welcome` 进程来显示欢迎界面。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Welcome1` |
| Object path | `/org/deepin/dde/Welcome1` |
| Interface | `org.deepin.dde.Welcome1` |
| Bus | Session |

### 服务激活

通过 D-Bus 服务激活机制启动欢迎界面进程：

- **功能**: 通过 D-Bus 服务名激活机制启动 `dde-welcome` 进程，实现欢迎界面的进程单实例控制
- **触发条件**: 当系统组件尝试调用此 D-Bus 服务名时自动触发，D-Bus 守护进程根据 `.service` 文件自动启动对应进程
- **使用场景**: 新用户首次登录或系统安装完成后，会话启动时通过此服务名激活欢迎程序以显示引导界面

```bash
gdbus call --session \
  --dest org.deepin.dde.Welcome1 \
  --object-path /org/deepin/dde/Welcome1 \
  --method org.freedesktop.DBus.Peer.Ping
```

> 该服务不导出业务方法，仅通过 D-Bus 服务名注册实现进程单实例控制。欢迎界面窗口由 `dde-welcome` 进程直接展示。
