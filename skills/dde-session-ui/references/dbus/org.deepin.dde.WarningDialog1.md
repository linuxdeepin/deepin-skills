# org.deepin.dde.WarningDialog1 接口参考

该接口为注册型 D-Bus 服务，用于警告对话框的进程单实例控制。进程通过注册 D-Bus 服务名实现单实例控制，但不导出业务方法。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.WarningDialog1` |
| Object path | `/org/deepin/dde/WarningDialog1` |
| Interface | `org.deepin.dde.WarningDialog1` |
| Bus | Session |

### 服务注册

通过注册型 D-Bus 服务实现警告对话框进程的单实例控制：

- **功能**: 进程启动时注册 D-Bus 服务名，实现警告对话框的进程单实例控制
- **触发条件**: 当 `dde-warning-dialog` 进程启动时自动注册服务名；后续启动的实例检测到服务名已被占用则直接退出
- **使用场景**: 系统检测到电池耗尽或磁盘空间不足严重警告条件时，启动 `dde-warning-dialog` 进程以显示警告窗口

```bash
gdbus call --session \
  --dest org.deepin.dde.WarningDialog1 \
  --object-path /org/deepin/dde/WarningDialog1 \
  --method org.freedesktop.DBus.Peer.Ping
```

> 该服务不导出业务方法，仅通过注册 D-Bus 服务名实现进程单实例控制。警告对话框窗口由 `dde-warning-dialog` 进程直接展示。
