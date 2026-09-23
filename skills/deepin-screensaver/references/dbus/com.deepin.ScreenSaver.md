# com.deepin.ScreenSaver 接口参考

该接口提供屏幕保护程序的启动、停止、预览、配置管理和屏保列表查询能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `com.deepin.ScreenSaver` |
| Object path | `/com/deepin/ScreenSaver` |
| Interface | `com.deepin.ScreenSaver` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 屏保启动与停止

#### Start

启动屏保。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.Start
```

#### Stop

停止屏保。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.Stop
```


### 预览与配置

#### Preview

预览指定屏保。

- **输入参数**: `name`（string, 类型 `s`）：屏保名称；`staysOn`（int32, 类型 `i`）：是否保持显示
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.Preview "DeepinScreensaver" 1
```

#### GetScreenSaverCover

获取指定屏保的封面图片路径。

- **输入参数**: `name`（string, 类型 `s`）：屏保名称
- **返回值**: `s`（string）：封面图片路径

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.GetScreenSaverCover "DeepinScreensaver"
```

#### StartCustomConfig

启动指定屏保的自定义配置。

- **输入参数**: `name`（string, 类型 `s`）：屏保名称
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.StartCustomConfig "DeepinScreensaver"
```

#### ConfigurableItems

获取可配置的屏保项列表。

- **输入参数**: 无
- **返回值**: `as`（string 数组）：可配置屏保名称列表

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.ConfigurableItems
```

#### IsConfigurable

查询指定屏保是否可配置。

- **输入参数**: `name`（string, 类型 `s`）：屏保名称
- **返回值**: `b`（bool）：是否可配置

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.IsConfigurable "DeepinScreensaver"
```

#### RefreshScreenSaverList

刷新屏保列表。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method com.deepin.ScreenSaver.RefreshScreenSaverList
```


### 屏保属性

#### isRunning（属性）

屏保是否正在运行。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver isRunning
```
#### currentScreenSaver（属性）

当前使用的屏保名称。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver currentScreenSaver
```
设置示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.ScreenSaver currentScreenSaver "<string>"
```
#### allScreenSaver（属性）

所有可用屏保列表。

| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver allScreenSaver
```
#### batteryScreenSaverTimeout（属性）

电池模式下屏保超时时间。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver batteryScreenSaverTimeout
```
设置示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.ScreenSaver batteryScreenSaverTimeout <int32 60>
```
#### linePowerScreenSaverTimeout（属性）

交流电源模式下屏保超时时间。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver linePowerScreenSaverTimeout
```
设置示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.ScreenSaver linePowerScreenSaverTimeout <int32 300>
```
#### lockScreenAtAwake（属性）

唤醒时是否锁定屏幕。

| 属性 | 值 |
|------|------|
| 类型 | `b` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver lockScreenAtAwake
```
设置示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.ScreenSaver lockScreenAtAwake <true>
```
#### lockScreenDelay（属性）

锁定屏幕延迟时间。

| 属性 | 值 |
|------|------|
| 类型 | `i` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Get \
  com.deepin.ScreenSaver lockScreenDelay
```
设置示例：

```bash
gdbus call --session \
  --dest com.deepin.ScreenSaver \
  --object-path /com/deepin/ScreenSaver \
  --method org.freedesktop.DBus.Properties.Set \
  com.deepin.ScreenSaver lockScreenDelay <int32 5>
```
---
