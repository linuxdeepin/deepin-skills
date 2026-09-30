# org.deepin.dde.KeyEvent1 接口参考

该接口提供按键事件监控能力，通过 D-Bus 信号广播允许列表内的按键事件（如触摸板切换、电源、蓝牙、无线、飞行模式、麦克风静音、屏幕锁定按键）。该接口不导出方法，仅提供信号。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.KeyEvent1` |
| Object path | `/org/deepin/dde/KeyEvent1` |
| Interface | `org.deepin.dde.KeyEvent1` |
| Bus | System |

### 信号

#### KeyEvent

当允许列表内的按键被按下或松开时发出此信号。

- **功能**：按键事件信号，通知有按键被按下或释放。
- **触发条件**：当系统检测到按键按下或释放事件时发出。
- **使用场景**：全局快捷键监听、按键事件处理。

| 参数 | 类型 | 说明 |
|------|------|------|
| keycode | `u`（uint32） | 按键码 |
| pressed | `b`（bool） | `true` 表示按下，`false` 表示松开 |
| ctrlPressed | `b`（bool） | Ctrl 键是否处于按下状态 |
| shiftPressed | `b`（bool） | Shift 键是否处于按下状态 |
| altPressed | `b`（bool） | Alt 键是否处于按下状态 |
| superPressed | `b`（bool） | Super（Meta）键是否处于按下状态 |

```bash
gdbus monitor --system \
  --dest org.deepin.dde.KeyEvent1 \
  --object-path /org/deepin/dde/KeyEvent1
```
