# org.deepin.dde.Display1 接口参考

该接口提供显示器配置、亮度、旋转和分辨率管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Display1` |
| Object path | `/org/deepin/dde/Display1` |
| Interface | `org.deepin.dde.Display1` |
| Bus | Session |
### 显示管理方法

#### ApplyChanges

应用显示配置变更。

- **功能**：应用当前未保存的显示配置变更到实际显示器输出。
- **触发条件**：当用户在显示设置中点击应用变更时调用。
- **使用场景**：控制中心显示设置应用配置变更。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display1 \
  --object-path /org/deepin/dde/Display1 \
  --method org.deepin.dde.Display1.ApplyChanges
```

#### ResetChanges

重置显示配置变更。

- **功能**：放弃当前未保存的显示配置变更，恢复到上次保存的配置。
- **触发条件**：当用户在显示设置中点击恢复默认或取消变更时调用。
- **使用场景**：控制中心显示设置取消未保存的变更。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display1 \
  --object-path /org/deepin/dde/Display1 \
  --method org.deepin.dde.Display1.ResetChanges
```

#### SwitchMode

切换显示模式。

- **功能**：切换显示模式（复制、扩展、仅主屏、仅副屏）。
- **触发条件**：当用户在显示设置中切换显示模式时调用。
- **使用场景**：控制中心显示设置切换多屏模式、快捷键切换显示模式。

- **输入参数**: `mode`（byte, 类型 `y`）：显示模式；`screenName`（string, 类型 `s`）：屏幕名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display1 \
  --object-path /org/deepin/dde/Display1 \
  --method org.deepin.dde.Display1.SwitchMode 0 "eDP-1"
```

#### Save

保存显示配置。

- **功能**：将当前显示配置保存为默认配置，重启后自动生效。
- **触发条件**：当用户在显示设置中确认保存配置时调用。
- **使用场景**：控制中心显示设置保存配置。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display1 \
  --object-path /org/deepin/dde/Display1 \
  --method org.deepin.dde.Display1.Save
```

#### AssociateTouch

关联触摸屏。

- **功能**：将触摸屏设备关联到指定的显示器输出。
- **触发条件**：当用户在显示设置中配置触摸屏映射时调用。
- **使用场景**：多屏触摸屏映射配置。

- **输入参数**: `screenName`（string, 类型 `s`）：屏幕名称；`touchScreen`（string, 类型 `s`）：触摸屏标识
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display1 \
  --object-path /org/deepin/dde/Display1 \
  --method org.deepin.dde.Display1.AssociateTouch "eDP-1" "touch0"
```

#### AssociateTouchByUUID

通过 UUID 关联触摸屏。

- **功能**：通过 UUID 将触摸屏设备关联到指定的显示器输出。
- **触发条件**：当用户在显示设置中通过 UUID 配置触摸屏映射时调用。
- **使用场景**：多屏触摸屏映射配置（使用 UUID 标识）。

- **输入参数**: `screenName`（string, 类型 `s`）：屏幕名称；`uuid`（string, 类型 `s`）：触摸屏 UUID
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display1 \
  --object-path /org/deepin/dde/Display1 \
  --method org.deepin.dde.Display1.AssociateTouchByUUID "eDP-1" "uuid"
```

#### ChangeBrightness

更改亮度。

- **功能**：调高或调低亮度。
- **触发条件**：当用户在显示设置或快捷面板调节亮度时调用。
- **使用场景**：控制中心亮度调节、快捷面板亮度滑块。

- **输入参数**: `raised`（bool, 类型 `b`）：是否调高亮度
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Display1 \
  --object-path /org/deepin/dde/Display1 \
  --method org.deepin.dde.Display1.ChangeBrightness true
```

