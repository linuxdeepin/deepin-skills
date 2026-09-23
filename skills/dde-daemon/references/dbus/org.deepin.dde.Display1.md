# org.deepin.dde.Display1 接口参考

该接口提供显示器配置、亮度、旋转和分辨率管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Display` |
| Object path | `/com/deepin/daemon/Display` |
| Interface | `org.deepin.dde.Display1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 显示管理方法

#### ApplyChanges

应用显示配置变更。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display \
  --object-path /com/deepin/daemon/Display \
  --method org.deepin.dde.Display1.ApplyChanges
```

#### ResetChanges

重置显示配置变更。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display \
  --object-path /com/deepin/daemon/Display \
  --method org.deepin.dde.Display1.ResetChanges
```

#### SwitchMode

切换显示模式。

- **输入参数**: `mode`（int32, 类型 `i`）：显示模式；`screenName`（string, 类型 `s`）：屏幕名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display \
  --object-path /com/deepin/daemon/Display \
  --method org.deepin.dde.Display1.SwitchMode 0 "eDP-1"
```

#### Save

保存显示配置。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display \
  --object-path /com/deepin/daemon/Display \
  --method org.deepin.dde.Display1.Save
```

#### AssociateTouch

关联触摸屏。

- **输入参数**: `screenName`（string, 类型 `s`）：屏幕名称；`touchScreen`（string, 类型 `s`）：触摸屏标识
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display \
  --object-path /com/deepin/daemon/Display \
  --method org.deepin.dde.Display1.AssociateTouch "eDP-1" "touch0"
```

#### AssociateTouchByUUID

通过 UUID 关联触摸屏。

- **输入参数**: `screenName`（string, 类型 `s`）：屏幕名称；`uuid`（string, 类型 `s`）：触摸屏 UUID
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display \
  --object-path /com/deepin/daemon/Display \
  --method org.deepin.dde.Display1.AssociateTouchByUUID "eDP-1" "uuid"
```

#### ChangeBrightness

更改亮度。

- **输入参数**: `brightness`（double, 类型 `d`）：亮度值
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display \
  --object-path /com/deepin/daemon/Display \
  --method org.deepin.dde.Display1.ChangeBrightness 0.5
```

