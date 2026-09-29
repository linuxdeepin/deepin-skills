# org.freedesktop.impl.portal.Background 接口参考

该接口提供后台运行管理能力，允许沙箱应用请求开机自启动、查询应用运行状态、通知后台运行状态。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Background` |
| Bus | Session |

### 后台管理方法

#### EnableAutostart

设置应用是否开机自启动。

- **功能**: 将指定应用注册为开机自启动或取消开机自启动。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求设置自身开机自启动状态时触发。
- **使用场景**: 沙箱应用需要配置自己在系统启动时自动运行时使用。
- **输入参数**: `app_id`（string, 类型 `s`）：应用 ID；`enable`（bool, 类型 `b`）：是否启用自启动；`commandline`（字符串数组, 类型 `as`）：启动命令行；`flags`（uint, 类型 `u`）：标志位
- **返回值**: `b`（bool）：是否设置成功

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Background.EnableAutostart "app" true [] 0
```

#### GetAppState

获取应用运行状态。

- **功能**: 返回所有已注册应用的运行状态映射。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端查询应用运行状态时触发。
- **使用场景**: 沙箱应用需要判断某个应用是否正在运行时使用。
- **输入参数**: 无
- **返回值**: `a{sv}`（字典）：应用状态映射（应用 ID → 运行状态）

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Background.GetAppState
```

#### NotifyBackground

通知后台运行状态。

- **功能**: 通知 portal 后端某应用正在请求后台运行，返回是否允许后台运行的响应。
- **触发条件**: 当沙箱应用通过 xdg-desktop-portal 前端请求在后台运行时触发。
- **使用场景**: 沙箱应用需要在用户关闭窗口后继续在后台运行时使用。
- **输入参数**: `handle`（object path, 类型 `o`）：请求句柄；`app_id`（string, 类型 `s`）：应用 ID；`name`（string, 类型 `s`）：通知名称
- **返回值**: `u`（uint）：响应码；`results`（字典, 类型 `a{sv}`）：通知结果

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Background.NotifyBackground "/" "app" "test"
```

### 信号

#### RunnintApplicationsChanged

当运行中的应用列表发生变化时触发。

- **功能**: 通知监听方运行中的应用列表已发生变化。
- **触发条件**: 当应用的启动或退出导致运行中的应用列表发生变化时触发。
- **使用场景**: 沙箱应用或桌面环境组件需要实时感知应用运行状态变化时监听此信号。
- **参数**: 无
