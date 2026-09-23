# org.deepin.dde.Grub2 接口参考

该接口提供 GRUB2 引导配置管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Grub2` |
| Object path | `/org/deepin/dde/Grub2` |
| Interface | `org.deepin.dde.Grub2` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### GRUB2 管理方法

#### Disable

禁用 GRUB2。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.Disable
```

#### Enable

启用 GRUB2。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.Enable
```

#### SkipGrub

跳过 GRUB2。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.SkipGrub
```

#### GetAvailableGfxmodes

获取可用图形模式。

- **输入参数**: 无
- **返回值**: `a(ss)`（元组数组）：图形模式列表

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.GetAvailableGfxmodes
```

#### GetSimpleEntryTitles

获取简单条目标题。

- **输入参数**: 无
- **返回值**: `as`（string 数组）：标题列表

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.GetSimpleEntryTitles
```

#### PrepareGfxmodeDetect

准备图形模式检测。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.PrepareGfxmodeDetect
```

#### Reset

重置 GRUB2 配置。

- **输入参数**: 无
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.Reset
```

#### SetDefaultEntry

设置默认条目。

- **输入参数**: `entry`（string, 类型 `s`）：条目标题
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.SetDefaultEntry "entry"
```

#### SetEnableTheme

设置是否启用主题。

- **输入参数**: `enable`（bool, 类型 `b`）：是否启用
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.SetEnableTheme true
```

#### SetGfxmode

设置图形模式。

- **输入参数**: `mode`（string, 类型 `s`）：图形模式
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.SetGfxmode "1920x1080"
```

#### SetTimeout

设置超时时间。

- **输入参数**: `timeout`（int32, 类型 `i`）：超时秒数
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.SetTimeout 5
```

#### GetBackground

获取背景图片。

- **输入参数**: 无
- **返回值**: `s`（string）：背景图片路径

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.GetBackground
```

#### SetBackgroundSourceFile

设置背景源文件。

- **输入参数**: `file`（string, 类型 `s`）：文件路径
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.Grub2 \
  --object-path /org/deepin/dde/Grub2 \
  --method org.deepin.dde.Grub2.SetBackgroundSourceFile "/path/to/bg"
```

