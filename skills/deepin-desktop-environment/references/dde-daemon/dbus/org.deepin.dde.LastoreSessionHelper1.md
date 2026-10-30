# org.deepin.dde.LastoreSessionHelper1 接口参考

该接口提供应用商店会话辅助能力，包括磁盘空间检查、系统代理获取、通知发送、通知关闭和日志上报。该服务在 Session 总线上导出 `Lastore` 对象，同时在 System 总线上导出 `Agent` 对象（由系统总线 Lastore 服务通过 `RegisterAgent` 注册调用）。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.LastoreSessionHelper1` |
| Object path | `/org/deepin/dde/LastoreSessionHelper1` |
| Interface | `org.deepin.dde.LastoreSessionHelper1` |
| Bus | Session |

### Lastore 对象方法

#### IsDiskSpaceSufficient

检查磁盘空间是否充足。

- **功能**：检查系统磁盘空间是否充足以进行应用安装或更新。
- **触发条件**：当应用商店在安装或更新应用前需要检查磁盘空间时调用。
- **使用场景**：应用商店安装应用前磁盘空间检查。

- **输入参数**: 无
- **返回值**: `result`（bool, 类型 `b`）：磁盘空间是否充足

```bash
gdbus call --session \
  --dest org.deepin.dde.LastoreSessionHelper1 \
  --object-path /org/deepin/dde/LastoreSessionHelper1 \
  --method org.deepin.dde.LastoreSessionHelper1.IsDiskSpaceSufficient
```

### Agent 对象

Agent 对象导出在 System 总线上，对象路径为 `/org/deepin/dde/Lastore1/Agent`，接口为 `org.deepin.dde.Lastore1.Agent`。Agent 由系统总线 Lastore 服务（`org.deepin.dde.Lastore1`）通过 `RegisterAgent` 注册，其方法由系统总线 Lastore 服务调用，不通过 `org.deepin.dde.LastoreSessionHelper1` 服务名直接访问。

| 字段 | 值 |
|------|------|
| Service | 进程唯一连接名（System 总线） |
| Object path | `/org/deepin/dde/Lastore1/Agent` |
| Interface | `org.deepin.dde.Lastore1.Agent` |
| Bus | System |

#### GetManualProxy

获取手动配置的系统代理信息。

- **功能**：获取手动配置的系统代理信息。
- **触发条件**：当应用商店需要获取系统代理设置进行网络请求时调用。
- **使用场景**：应用商店通过系统代理下载应用。

- **输入参数**: 无
- **返回值**: `outArg0`（`a{ss}`，map[string]string）：代理信息，键为代理类型（`http`、`https`、`ftp`、`socks`），值为代理地址

#### SendNotify

发送桌面通知。

- **功能**：发送桌面通知。
- **触发条件**：当应用商店需要通知用户下载或安装状态时调用。
- **使用场景**：应用商店下载完成通知、安装失败通知。

- **输入参数**:
  - `appName`（string, 类型 `s`）：应用名称
  - `replacesId`（uint32, 类型 `u`）：替换的通知 ID，`0` 表示新通知
  - `appIcon`（string, 类型 `s`）：应用图标
  - `summary`（string, 类型 `s`）：通知摘要
  - `body`（string, 类型 `s`）：通知正文
  - `actions`（`as`，[]string）：通知动作列表
  - `hints`（`a{sv}`，map[string]dbus.Variant）：通知提示信息
  - `expireTimeout`（int32, 类型 `i`）：过期超时时间（毫秒），`-1` 表示默认，`0` 表示不自动隐藏
- **返回值**: `outArg0`（uint32, 类型 `u`）：通知 ID

#### CloseNotification

关闭指定通知。

- **功能**：关闭指定通知。
- **触发条件**：当应用商店需要关闭已发送的通知时调用。
- **使用场景**：应用商店关闭过期或不再需要的通知。

- **输入参数**: `id`（uint32, 类型 `u`）：通知 ID
- **返回值**: 无

#### ReportLog

上报日志信息。

- **功能**：上报日志信息。
- **触发条件**：当应用商店需要记录操作日志时调用。
- **使用场景**：应用商店操作日志记录。

- **输入参数**: `msg`（string, 类型 `s`）：日志消息
- **返回值**: 无
