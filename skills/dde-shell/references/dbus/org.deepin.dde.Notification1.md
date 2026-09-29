# org.deepin.dde.Notification1 接口参考

该接口完整提供桌面通知能力，并扩展应用通知配置、系统通知配置和通知记录状态查询。可用于查询通知能力、发送和关闭通知、查询通知服务器信息、管理应用与系统通知配置、读取通知记录数量，以及监听通知与配置变化。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Notification1` |
| Object path | `/org/deepin/dde/Notification1` |
| Interface | `org.deepin.dde.Notification1` |
| Bus | Session |

## 接口关系

dde-shell 的通知服务注册了以下 D-Bus 服务接口：

- `org.freedesktop.Notifications`（`/org/freedesktop/Notifications`）— freedesktop 标准通知接口，仅提供通知发送（`Notify`）、关闭（`CloseNotification`）、能力查询（`GetCapabilities`）和服务器信息查询（`GetServerInformation`）功能。

**扩充关系**：`org.deepin.dde.Notification1`（`/org/deepin/dde/Notification1`）在 `org.freedesktop.Notifications` 基础上扩充了应用通知管理（`GetAppList`、`GetAppInfo`、`SetAppInfo`、`GetAppSetting`、`SetAppSetting`）、系统通知配置（`SetSystemInfo`、`GetSystemInfo`）和通知记录管理（`recordCount` 属性）功能。两个接口共用同一通知服务实现。

**兼容关系**：`org.freedesktop.Notifications` 为兼容 freedesktop 通知规范的应用而保留，功能与 `org.deepin.dde.Notification1` 的通知操作部分相同，但不包含 DDE 扩展功能。新代码应优先使用 `org.deepin.dde.Notification1`。

## 方法、属性与信号

### 桌面通知操作

#### GetCapabilities

获取通知服务器支持的能力列表。

- **功能**: 查询通知服务器支持哪些能力（如动作按钮、静态图标、持久化、Body 内容标记）
- **触发条件**: 外部程序调用此方法时执行
- **使用场景**: 应用在发送通知前查询服务器支持的能力，以决定通知的展示方式
- **输入参数**: 无
- **返回值**: `as`（string 数组）：能力名称列表

```bash
gdbus call --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1 \
  --method org.deepin.dde.Notification1.GetCapabilities
```

#### Notify

发送桌面通知，或使用已有通知 ID 替换通知。

- **功能**: 向桌面通知服务发送一条通知，若指定已有通知 ID 则替换该通知的内容
- **触发条件**: 外部程序调用此方法时执行
- **使用场景**: 应用向用户展示桌面通知消息，或更新已发送通知的标题、正文、图标内容
- **输入参数**:
  - `appName`（string, 类型 `s`）：应用名称
  - `replacesId`（uint, 类型 `u`）：要替换的通知 ID，`0` 表示创建通知
  - `appIcon`（string, 类型 `s`）：应用图标路径或图标名称
  - `summary`（string, 类型 `s`）：通知标题
  - `body`（string, 类型 `s`）：通知正文
  - `actions`（string 数组, 类型 `as`）：动作键与动作标题组成的列表
  - `hints`（字典, 类型 `a{sv}`）：通知提示信息
  - `expireTimeout`（int32, 类型 `i`）：超时时间，单位为毫秒；`-1` 使用服务器默认值
- **返回值**: `u`（uint）：通知 ID

```bash
gdbus call --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1 \
  --method org.deepin.dde.Notification1.Notify \
  "my-app" 0 "dialog-information" "通知标题" "通知正文" \
  "['open', '打开']" "{}" 5000
```

#### CloseNotification

关闭指定通知。

- **功能**: 根据通知 ID 关闭已发送的桌面通知
- **触发条件**: 外部程序调用此方法时执行
- **使用场景**: 应用在通知不再需要时主动关闭已发送的通知（如消息已读后关闭通知气泡）
- **输入参数**:
  - `id`（uint, 类型 `u`）：通知 ID
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1 \
  --method org.deepin.dde.Notification1.CloseNotification 1
```

#### GetServerInformation

获取通知服务器的名称、厂商、版本和所实现的通知规范版本。

- **功能**: 查询通知服务器的名称、厂商、版本和通知规范版本
- **触发条件**: 外部程序调用此方法时执行
- **使用场景**: 调试或兼容性检测时确认通知服务器的身份和版本
- **输入参数**: 无
- **返回值**: `(ssss)`：服务器名称、厂商、版本、通知规范版本

```bash
gdbus call --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1 \
  --method org.deepin.dde.Notification1.GetServerInformation
```

### 应用通知配置

#### GetAppList

获取已注册通知的应用列表。

- **功能**: 查询当前已注册通知服务的应用 ID 列表
- **触发条件**: 外部程序调用此方法时执行
- **使用场景**: 通知设置界面展示已发送过通知的应用列表，供用户逐应用配置通知开关
- **输入参数**: 无
- **返回值**: `as`（string 数组）：应用 ID 列表

```bash
gdbus call --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1 \
  --method org.deepin.dde.Notification1.GetAppList
```

#### GetAppInfo

获取指定应用的通知配置项。

- **功能**: 读取指定应用的某个通知配置项的值
- **触发条件**: 外部程序调用此方法时执行
- **使用场景**: 通知设置界面读取某应用的通知开关、声音、横幅展示配置
- **输入参数**:
  - `appId`（string, 类型 `s`）：应用 ID
  - `configItem`（uint, 类型 `u`）：配置项编号
- **返回值**: `v`（variant）：配置值

```bash
gdbus call --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1 \
  --method org.deepin.dde.Notification1.GetAppInfo "my-app" 0
```

#### SetAppInfo

设置指定应用的通知配置项。

- **功能**: 修改指定应用的某个通知配置项的值
- **触发条件**: 外部程序调用此方法时执行；设置成功后会发出 `AppInfoChanged` 信号
- **使用场景**: 通知设置界面修改某应用的通知开关、声音、横幅展示配置
- **输入参数**:
  - `appId`（string, 类型 `s`）：应用 ID
  - `configItem`（uint, 类型 `u`）：配置项编号
  - `value`（variant, 类型 `v`）：新值
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1 \
  --method org.deepin.dde.Notification1.SetAppInfo \
  "my-app" 0 "<true>"
```

#### GetAppSetting

获取指定应用的通知设置 JSON。

- **功能**: 读取指定应用的完整通知设置，以 JSON 字符串形式返回
- **触发条件**: 外部程序调用此方法时执行
- **使用场景**: 批量读取某应用的全部通知设置（如开关、声音、横幅、免打扰），用于设置界面初始化或配置导出
- **输入参数**:
  - `appName`（string, 类型 `s`）：应用名称
- **返回值**: `s`（string）：通知设置 JSON 字符串

```bash
gdbus call --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1 \
  --method org.deepin.dde.Notification1.GetAppSetting "my-app"
```

#### SetAppSetting

设置应用通知设置。

- **功能**: 以 JSON 字符串形式批量修改指定应用的通知设置
- **触发条件**: 外部程序调用此方法时执行
- **使用场景**: 批量写入某应用的全部通知设置（如开关、声音、横幅、免打扰），用于设置界面保存或配置导入
- **输入参数**:
  - `settings`（string, 类型 `s`）：通知设置 JSON 字符串
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1 \
  --method org.deepin.dde.Notification1.SetAppSetting '"{\"app\":\"my-app\",\"enabled\":true}"'
```

### 系统通知配置

#### SetSystemInfo

设置系统级通知配置项。

- **功能**: 修改系统级通知配置项的值（对全部应用生效）
- **触发条件**: 外部程序调用此方法时执行；设置成功后会发出 `SystemInfoChanged` 信号
- **使用场景**: 系统通知设置界面修改全局通知配置（如全局免打扰、全局通知开关）
- **输入参数**:
  - `configItem`（uint, 类型 `u`）：配置项编号
  - `value`（variant, 类型 `v`）：新值
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1 \
  --method org.deepin.dde.Notification1.SetSystemInfo 0 "<true>"
```

#### GetSystemInfo

获取系统级通知配置项。

- **功能**: 读取系统级通知配置项的值（对全部应用生效）
- **触发条件**: 外部程序调用此方法时执行
- **使用场景**: 系统通知设置界面读取全局通知配置（如全局免打扰、全局通知开关）
- **输入参数**:
  - `configItem`（uint, 类型 `u`）：配置项编号
- **返回值**: `v`（variant）：配置值

```bash
gdbus call --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1 \
  --method org.deepin.dde.Notification1.GetSystemInfo 0
```

### 通知记录状态

#### recordCount（属性）

当前通知记录数量。

- **功能**: 表示通知中心当前保存的通知记录总数
- **触发条件**: 通知记录增加或减少时值发生变化，同时发出 `RecordCountChanged` 信号
- **使用场景**: 通知中心面板显示未读通知数量角标
- **属性值**:

| 属性 | 值 |
|------|------|
| 类型 | `u`（uint） |
| 读写权限 | read |

```bash
gdbus call --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1 \
  --method org.freedesktop.DBus.Properties.Get \
  "org.deepin.dde.Notification1" "recordCount"
```

### 通知事件信号

#### ActionInvoked

用户触发通知动作时发出。

- **功能**: 通知用户在通知上点击了动作按钮，传递通知 ID 和动作键
- **触发条件**: 用户点击通知上的动作按钮时触发
- **使用场景**: 应用监听用户在通知上的交互行为，执行对应动作（如点击"打开"按钮后启动应用窗口）
- **参数**:
  - `id`（uint, 类型 `u`）：通知 ID
  - `actionKey`（string, 类型 `s`）：动作键

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1
```

#### NotificationClosed

通知关闭时发出。

- **功能**: 通知被关闭时通知调用方，传递通知 ID 和关闭原因
- **触发条件**: 通知过期、用户手动关闭、调用 `CloseNotification` 时触发
- **使用场景**: 应用监听通知关闭事件，清理与通知相关的资源或更新 UI 状态
- **参数**:
  - `id`（uint, 类型 `u`）：通知 ID
  - `reason`（uint, 类型 `u`）：关闭原因；`1` 表示过期，`2` 表示用户关闭，`3` 表示调用方关闭，`4` 表示原因未定义

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1
```

#### ActivationToken

通知激活并产生激活令牌时发出。

- **功能**: 通知被点击激活时传递 xdg-activation token，用于安全地激活应用窗口
- **触发条件**: 通知被点击激活且系统提供 xdg-activation token 时触发
- **使用场景**: 应用收到 token 后使用该 token 安全地将自身窗口置于前台
- **参数**:
  - `id`（uint, 类型 `u`）：通知 ID
  - `token`（string, 类型 `s`）：激活令牌

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1
```

### 配置与状态变化信号

#### AppAdded

新应用注册通知时发出。

- **功能**: 通知外部程序有新应用首次发送了通知
- **触发条件**: 有新应用首次发送通知时发出
- **使用场景**: 通知设置界面动态更新应用列表，将新应用加入设置页面
- **参数**:
  - `appId`（string, 类型 `s`）：应用 ID

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1
```

#### AppRemoved

应用被移除时发出。

- **功能**: 通知外部程序某应用已从通知列表中移除
- **触发条件**: 应用被从通知列表中移除时发出
- **使用场景**: 通知设置界面动态更新应用列表，将已移除的应用从设置页面删除
- **参数**:
  - `appId`（string, 类型 `s`）：应用 ID

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1
```

#### AppInfoChanged

应用通知配置变化时发出。

- **功能**: 通知外部程序某应用的通知配置项发生了变化，传递应用 ID、配置项编号和新值
- **触发条件**: 调用 `SetAppInfo` 后发出
- **使用场景**: 通知设置界面监听配置变化并实时更新 UI 显示
- **参数**:
  - `appId`（string, 类型 `s`）：应用 ID
  - `configItem`（uint, 类型 `u`）：配置项编号
  - `value`（variant, 类型 `v`）：新值

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1
```

#### AppSettingChanged

> ⚠️ **当前未实现**：已声明但从未 emit，当前不会触发。

应用通知设置变化时发出。

- **功能**: 通知外部程序某应用的通知设置 JSON 发生了变化
- **触发条件**: 调用 `SetAppSetting` 后应触发（当前未实现）
- **使用场景**: 通知设置界面监听应用设置的批量变化
- **参数**:
  - `settings`（string, 类型 `s`）：设置 JSON 字符串

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1
```

#### SystemSettingChanged

> ⚠️ **当前未实现**：已声明但从未 emit，当前不会触发。

系统通知设置变化时发出。

- **功能**: 通知外部程序系统通知设置 JSON 发生了变化
- **触发条件**: 系统通知设置被修改后应触发（当前未实现）
- **使用场景**: 通知设置界面监听系统设置的批量变化
- **参数**:
  - `settings`（string, 类型 `s`）：设置 JSON 字符串

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1
```

#### SystemInfoChanged

系统级通知配置变化时发出。

- **功能**: 通知外部程序某系统级通知配置项发生了变化，传递配置项编号和新值
- **触发条件**: 调用 `SetSystemInfo` 后发出
- **使用场景**: 通知设置界面监听系统级配置变化并实时更新 UI 显示
- **参数**:
  - `configItem`（uint, 类型 `u`）：配置项编号
  - `value`（variant, 类型 `v`）：新值

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1
```

#### NotificationStateChanged

通知处理状态变化时发出。

- **功能**: 通知外部程序某条通知的处理状态发生了变化，传递通知 ID 和处理类型
- **触发条件**: 通知被处理（显示、关闭）时发出
- **使用场景**: 通知中心或外部程序跟踪通知的生命周期状态（已显示、已关闭）
- **参数**:
  - `id`（int64, 类型 `x`）：通知 ID
  - `processedType`（int32, 类型 `i`）：处理类型

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1
```

#### RecordCountChanged

通知记录数量变化时发出。

- **功能**: 通知外部程序通知记录数量发生了变化，传递新的记录数量
- **触发条件**: 通知记录增加或减少时发出
- **使用场景**: 通知中心面板或任务栏角标实时更新未读通知数量
- **参数**:
  - `count`（uint, 类型 `u`）：新的记录数量

```bash
gdbus monitor --session \
  --dest org.deepin.dde.Notification1 \
  --object-path /org/deepin/dde/Notification1
```

---
