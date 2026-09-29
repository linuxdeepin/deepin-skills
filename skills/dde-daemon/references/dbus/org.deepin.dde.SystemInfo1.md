# org.deepin.dde.SystemInfo1 接口参考

该接口提供系统硬件和软件信息查询能力。该接口仅导出属性，无导出方法，属性通过 `org.freedesktop.DBus.Properties.Get` 访问。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.SystemInfo1` |
| Object path | `/org/deepin/dde/SystemInfo1` |
| Interface | `org.deepin.dde.SystemInfo1` |
| Bus | System |

### 系统信息属性

以下属性通过 `org.freedesktop.DBus.Properties.Get` 访问，均为只读。

#### MemorySize（属性）

内存大小（字节）。

- **功能**：获取系统物理内存大小，返回字节数。
- **触发条件**：属性，当内存配置变化时通过 PropertiesChanged 信号通知。
- **使用场景**：系统信息页面显示内存容量。

| 属性 | 值 |
|------|------|
| 类型 | `t`（uint64） |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.SystemInfo1 \
  --object-path /org/deepin/dde/SystemInfo1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SystemInfo1 MemorySize
```

#### MemorySizeHuman（属性）

内存大小（人类可读，如 `16.00GB`）。

- **功能**：获取系统物理内存大小的人类可读字符串。
- **触发条件**：属性，当内存配置变化时通过 PropertiesChanged 信号通知。
- **使用场景**：系统信息页面显示内存容量。

| 属性 | 值 |
|------|------|
| 类型 | `s`（string） |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.SystemInfo1 \
  --object-path /org/deepin/dde/SystemInfo1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SystemInfo1 MemorySizeHuman
```

#### CurrentSpeed（属性）

CPU 当前频率（MHz）。

- **功能**：获取 CPU 当前运行频率。
- **触发条件**：属性，当 CPU 频率变化时通过 PropertiesChanged 信号通知。
- **使用场景**：系统信息页面显示 CPU 频率。

| 属性 | 值 |
|------|------|
| 类型 | `t`（uint64） |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.SystemInfo1 \
  --object-path /org/deepin/dde/SystemInfo1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SystemInfo1 CurrentSpeed
```

#### DisplayDriver（属性）

显卡驱动。

- **功能**：获取当前显卡驱动名称。
- **触发条件**：属性，当显卡驱动变化时通过 PropertiesChanged 信号通知。
- **使用场景**：系统信息页面显示显卡驱动信息。

| 属性 | 值 |
|------|------|
| 类型 | `s`（string） |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.SystemInfo1 \
  --object-path /org/deepin/dde/SystemInfo1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SystemInfo1 DisplayDriver
```

#### VideoDriver（属性）

视频驱动。

- **功能**：获取当前视频驱动名称。
- **触发条件**：属性，当视频驱动变化时通过 PropertiesChanged 信号通知。
- **使用场景**：系统信息页面显示视频驱动信息。

| 属性 | 值 |
|------|------|
| 类型 | `s`（string） |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.SystemInfo1 \
  --object-path /org/deepin/dde/SystemInfo1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SystemInfo1 VideoDriver
```

#### DMIInfo（属性）

DMI 信息。

- **功能**：获取系统 DMI 信息，包含 BIOS 厂商、BIOS 版本、BIOS 日期、主板名称、主板序列号、主板厂商、主板版本、产品名称、产品系列、产品序列号、产品 UUID、产品版本。
- **触发条件**：属性，DMI 信息为硬件固定值，通常不变化。
- **使用场景**：系统信息页面显示硬件详细信息。

| 属性 | 值 |
|------|------|
| 类型 | `(ssssssssssss)`（结构体） |
| 读写权限 | read |

读取示例：

```bash
gdbus call --system \
  --dest org.deepin.dde.SystemInfo1 \
  --object-path /org/deepin/dde/SystemInfo1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.SystemInfo1 DMIInfo
```

#### 读取所有属性

```bash
gdbus call --system \
  --dest org.deepin.dde.SystemInfo1 \
  --object-path /org/deepin/dde/SystemInfo1 \
  --method org.freedesktop.DBus.Properties.GetAll \
  org.deepin.dde.SystemInfo1
```
