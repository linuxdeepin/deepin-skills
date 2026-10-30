# org.freedesktop.ScreenSaver 接口参考

管理当前会话的空闲计时、空闲抑制和用户活动模拟。屏保动画由屏保组件提供；本接口不解除锁屏认证，也不提供关机、休眠抑制。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.ScreenSaver` |
| Object path | `/org/freedesktop/ScreenSaver` |
| Interface | `org.freedesktop.ScreenSaver` |
| Bus | Session |

以下描述针对 dde-daemon 提供的服务实现。服务初始化需要可连接的 X 服务；Wayland 会话中的超时设置转发给 `org.deepin.dde.KWayland1.Idle.SetIdleTimeout`，不能据此保证纯 Wayland 或 Treeland 会话可用。接口不提供 `ActiveChanged` 信号。

## 方法

### Inhibit

暂停会话空闲计时，返回用于释放抑制的 cookie。适用于播放视频或展示内容期间保持会话活动。

- 输入：`name`（`s`），调用程序名称；`reason`（`s`），抑制原因。
- 返回：`cookie`（`u`），本次抑制标识。
- cookie 绑定调用方的 D-Bus 唯一连接名；使用同一连接调用 `UnInhibit`。独立的两次 `gdbus call` 不共享连接，不能用来完成这个生命周期。
- 每次调用分别保存 cookie 并显式释放。连接断开时存在清理处理，但同一连接多次申请的全部抑制不保证均被清理。

风险警示：
- 暂停空闲计时会影响依赖该计时的自动屏保或自动锁屏；使用结束后应释放抑制。

用例（需要 Python 3、PyGObject 和 Gio；在当前用户会话运行）：

```python
from gi.repository import Gio, GLib

bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
service = 'org.freedesktop.ScreenSaver'
path = '/org/freedesktop/ScreenSaver'
interface = 'org.freedesktop.ScreenSaver'

def call(method, params, result_type):
    return bus.call_sync(
        service, path, interface, method, params,
        GLib.VariantType.new(result_type),
        Gio.DBusCallFlags.NONE, 5000, None)

cookie, = call('Inhibit', GLib.Variant('(ss)',
    ('presentation', '用户正在演示')), '(u)').unpack()
try:
    input('演示结束后按回车释放空闲抑制：')
finally:
    call('UnInhibit', GLib.Variant('(u)', (cookie,)), '()')
```

### UnInhibit

取消本连接申请的指定抑制；最后一个抑制释放后恢复计时设置。

- 输入：`cookie`（`u`），本连接的 `Inhibit` 返回值。
- 返回：无；cookie 不存在或属于其他连接时返回 D-Bus 错误。
- 用例见上面的 `finally` 块。不能使用固定数字或另一进程返回的 cookie。

### SimulateUserActivity

通过 X 屏保扩展模拟活动并重置空闲计时。适用于接收远程输入后更新本地活动状态；不模拟实际键盘或鼠标事件，也不解锁会话。该方法不转发到 Wayland 空闲接口。

- 输入：无。
- 返回：无；X 请求失败时返回 D-Bus 错误。

```bash
gdbus call --session \
  --dest org.freedesktop.ScreenSaver \
  --object-path /org/freedesktop/ScreenSaver \
  --method org.freedesktop.ScreenSaver.SimulateUserActivity
```

### SetTimeout

DDE 扩展：修改当前会话空闲计时参数。有活动抑制时暂存最新参数，在抑制释放后应用。

- 输入：`seconds`（`u`），空闲超时秒数，`0` 关闭计时；`interval`（`u`），X 屏保周期秒数；`blank`（`b`），X 屏保黑屏偏好。
- X11 后端将两个时间值转换为有符号 16 位整数，正数使用 `1–32767`，避免超出范围后发生截断。黑屏偏好是否生效由 X 服务决定。
- Wayland 转发仅传递 `seconds × 1000` 毫秒；`interval` 与 `blank` 不传递给该后端。
- 返回：无。底层设置失败只记录日志，方法成功返回不保证设置已生效。

风险警示：
- 修改会话空闲策略会影响依赖计时的自动屏保或自动锁屏；X11 调用还会将 DPMS 三项超时清零。

```bash
gdbus call --session \
  --dest org.freedesktop.ScreenSaver \
  --object-path /org/freedesktop/ScreenSaver \
  --method org.freedesktop.ScreenSaver.SetTimeout 300 0 false
```

## 信号

以下均为无参数的 DDE 扩展信号，由 X 屏保事件触发。它们不代表用户认证状态，也不保证收到 Wayland 合成器的活动变化。

| 信号 | 触发条件与用途 |
|------|----------------|
| `IdleOn` | X 屏保进入激活状态，供界面响应空闲状态 |
| `CycleActive` | X 屏保发生周期事件，供屏保更新展示内容 |
| `IdleOff` | X 屏保退出激活状态，供界面响应恢复活动 |

用例：监听上述三个信号。

```bash
gdbus monitor --session \
  --dest org.freedesktop.ScreenSaver \
  --object-path /org/freedesktop/ScreenSaver
```
