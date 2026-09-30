# org.deepin.ds.Dock 接口参考

该接口是提供给外部控制 Dock 的服务接口，允许外部程序读取和设置 Dock 的位置、几何区域和是否在主屏显示属性。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.ds.Dock` |
| Object path | `/org/deepin/ds/Dock` |
| Interface | `org.deepin.ds.Dock` |
| Bus | Session |

## 接口关系

Dock 面板服务除当前使用的 `org.deepin.ds.Dock` 外，还注册了两个历史别名服务，各自注册在独立的对象路径上，用于向后兼容不同版本的调用方：

- `org.deepin.ds.Dock`（`/org/deepin/ds/Dock`）— 当前服务名。
- `org.deepin.dde.Dock1`（`/org/deepin/dde/Dock1`）— 旧版前端接口别名。
- `org.deepin.dde.daemon.Dock1`（`/org/deepin/dde/daemon/Dock1`）— 旧版守护进程接口别名。

**兼容关系**：`org.deepin.dde.Dock1` 和 `org.deepin.dde.daemon.Dock1` 为兼容历史调用方而保留，功能与 `org.deepin.ds.Dock` 相同。新代码应优先使用 `org.deepin.ds.Dock`。

## 方法、属性与信号

### Dock 属性

#### geometry（属性）

Dock 的几何区域。

- **功能**: 表示 Dock 面板当前的几何区域（x 坐标、y 坐标、宽度、高度）
- **触发条件**: Dock 面板位置或大小变化时值随之更新
- **使用场景**: 外部程序（如窗口管理器）需要获取 Dock 占用的屏幕区域以避免窗口遮挡
- **属性值**:

| 属性 | 值 |
|------|------|
| 类型 | `(iiii)`（QRect: x, y, width, height） |
| 读写权限 | read |

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock \
  --object-path /org/deepin/ds/Dock \
  --method org.freedesktop.DBus.Properties.Get \
  "org.deepin.ds.Dock" "geometry"
```

#### position（属性）

Dock 位置。

- **功能**: 表示 Dock 面板在屏幕上的位置（底部、顶部、左侧、右侧）
- **触发条件**: 外部程序通过 Properties.Set 修改时更新；Dock 面板位置变化时值随之更新
- **使用场景**: Dock 设置界面读取和修改 Dock 的显示位置
- **属性值**:

| 属性 | 值 |
|------|------|
| 类型 | `i`（int32） |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock \
  --object-path /org/deepin/ds/Dock \
  --method org.freedesktop.DBus.Properties.Get \
  "org.deepin.ds.Dock" "position"
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock \
  --object-path /org/deepin/ds/Dock \
  --method org.freedesktop.DBus.Properties.Set \
  "org.deepin.ds.Dock" "position" "<int32 0>"
```

#### showInPrimary（属性）

是否在主屏显示 Dock。

- **功能**: 控制 Dock 面板是否仅在主显示器上显示
- **触发条件**: 外部程序通过 Properties.Set 修改时更新
- **使用场景**: 多显示器环境下，用户通过 Dock 设置控制 Dock 是否仅在主屏显示
- **属性值**:

| 属性 | 值 |
|------|------|
| 类型 | `b`（bool） |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock \
  --object-path /org/deepin/ds/Dock \
  --method org.freedesktop.DBus.Properties.Get \
  "org.deepin.ds.Dock" "showInPrimary"
```

设置示例：

```bash
gdbus call --session \
  --dest org.deepin.ds.Dock \
  --object-path /org/deepin/ds/Dock \
  --method org.freedesktop.DBus.Properties.Set \
  "org.deepin.ds.Dock" "showInPrimary" "<true>"
```

---
