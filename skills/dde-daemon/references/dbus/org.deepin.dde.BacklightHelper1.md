# org.deepin.dde.BacklightHelper1 接口参考

该接口提供背光亮度和 DDCCI 管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.BacklightHelper1` |
| Object path | `/org/deepin/dde/BacklightHelper1` |
| Interface | `org.deepin.dde.BacklightHelper1` |
| Bus | System |
### 背光辅助方法

#### CheckCfgSupport

检查配置是否支持。

- **功能**：检查指定背光配置是否支持。
- **触发条件**：当需要确认某设备是否支持特定背光配置时调用。
- **使用场景**：背光设备能力查询，确认设备支持的背光类型。
- **输入参数**: `name`（string, 类型 `s`）：配置名称
- **返回值**: `b`（bool）：是否支持

```bash
gdbus call --system \
  --dest org.deepin.dde.BacklightHelper1 \
  --object-path /org/deepin/dde/BacklightHelper1 \
  --method org.deepin.dde.BacklightHelper1.CheckCfgSupport "ddcci"
```

#### SetBrightness

设置背光亮度。

- **功能**：设置屏幕背光亮度值。
- **触发条件**：当用户在控制中心或快捷面板调节亮度时调用。
- **使用场景**：控制中心亮度调节、快捷面板亮度滑块。

- **输入参数**: `type0`（byte, 类型 `y`）：背光类型（1=显示背光，2=键盘背光）；`name`（string, 类型 `s`）：设备名称；`value`（int32, 类型 `i`）：亮度值
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.BacklightHelper1 \
  --object-path /org/deepin/dde/BacklightHelper1 \
  --method org.deepin.dde.BacklightHelper1.SetBrightness 1 "intel_backlight" 50
```
