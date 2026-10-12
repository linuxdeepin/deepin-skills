# org.deepin.dde.LocaleHelper1 接口参考

该接口提供系统区域设置生成和切换能力。

> **使用提示**：该服务无法通过 D-Bus 自动激活，需确保对应的 systemd 服务已启动后再进行 D-Bus 调用。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.LocaleHelper1` |
| Object path | `/org/deepin/dde/LocaleHelper1` |
| Interface | `org.deepin.dde.LocaleHelper1` |
| Bus | System |

## 区域设置方法

### GenerateLocale

生成指定的区域设置。该方法执行完毕后会发出 `Success` 信号通知结果。

- **功能**: 根据指定的区域名称生成对应的系统区域设置（locale）
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 控制中心区域设置中选择新语言后生成对应的 locale 数据

- **输入参数**:
  - `locale`（string, 类型 `s`）：区域名称（如 `zh_CN.UTF-8`）
- **返回值**: 无（出错时返回 dbus.Error）
- **信号**: 完成后发出 `Success(ok bool, reason string)` 信号

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.LocaleHelper1 \
  --object-path /org/deepin/dde/LocaleHelper1 \
  --method org.deepin.dde.LocaleHelper1.GenerateLocale \
  "zh_CN.UTF-8"
```

### SetLocale

设置系统区域。

- **功能**: 将系统当前区域设置切换为指定的区域名称
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 控制中心切换系统语言和区域格式

- **输入参数**:
  - `locale`（string, 类型 `s`）：区域名称（如 `zh_CN.UTF-8`）
- **返回值**: 无（出错时返回 dbus.Error）

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.LocaleHelper1 \
  --object-path /org/deepin/dde/LocaleHelper1 \
  --method org.deepin.dde.LocaleHelper1.SetLocale \
  "zh_CN.UTF-8"
```

### SetAllowCaller

将指定 D-Bus 连接名添加到允许调用者列表。

- **功能**: 将指定的 D-Bus 唯一连接名添加到 LocaleHelper1 的允许调用者列表中，授权其调用该接口的方法
- **触发条件**: 由需要授权其他连接调用 LocaleHelper1 的特权进程调用
- **使用场景**: 桌面会话管理器授权子服务调用区域设置接口

- **输入参数**:
  - `uniqueName`（string, 类型 `s`）：待授权的 D-Bus 唯一连接名
- **返回值**: 无（出错时返回 dbus.Error）

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.LocaleHelper1 \
  --object-path /org/deepin/dde/LocaleHelper1 \
  --method org.deepin.dde.LocaleHelper1.SetAllowCaller \
  ":1.42"
```

## 信号

### Success

`GenerateLocale` 方法执行完毕后发出此信号，通知操作结果。

- **功能**: 通知调用方区域设置生成操作的执行结果
- **触发条件**: `GenerateLocale` 方法执行完成后触发
- **使用场景**: 调用方在发起 `GenerateLocale` 后监听此信号以获取生成结果，从而决定后续操作（如提示用户成功或失败）

- **参数**:
  - `ok`（bool, 类型 `b`）：操作是否成功
  - `reason`（string, 类型 `s`）：失败原因（成功时为空字符串）

```bash
gdbus monitor --system \
  --dest org.deepin.dde.LocaleHelper1 \
  --object-path /org/deepin/dde/LocaleHelper1
```
