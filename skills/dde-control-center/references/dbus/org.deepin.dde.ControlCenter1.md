# org.deepin.dde.ControlCenter1 接口参考

该接口提供控制中心窗口的显示、隐藏、切换、退出、页面跳转和模块列表获取能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ControlCenter1` |
| Object path | `/org/deepin/dde/ControlCenter1` |
| Interface | `org.deepin.dde.ControlCenter1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 窗口显示控制

#### Show

显示控制中心窗口。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.Show
```

#### Hide

隐藏控制中心窗口。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.Hide
```

#### Toggle

切换控制中心窗口显示状态。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.Toggle
```

#### Exit

退出控制中心。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.Exit
```

#### ShowHome

显示控制中心首页。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.ShowHome
```


### 页面跳转

#### ShowPage

跳转到指定 URL 对应的页面。

- **输入参数**: `url`（string, 类型 `s`）：页面 URL
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.ShowPage "display"
```

#### ShowPage

跳转到指定模块和页面（已弃用）。

- **输入参数**: `module`（string, 类型 `s`）：模块名称；`page`（string, 类型 `s`）：页面名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.ShowPage "display" "brightness"
```

#### ShowModule

跳转到指定模块（已弃用）。

- **输入参数**: `module`（string, 类型 `s`）：模块名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.ShowModule "display"
```

#### GetAllModule

获取所有模块信息。

- **输入参数**: 无
- **返回值**: `s`（string）：模块信息 JSON

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.GetAllModule
```


### 窗口属性

#### Rect（属性）

控制中心窗口的矩形区域。

| 属性 | 值 |
|------|------|
| 类型 | `(iiii)` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.ControlCenter1 Rect
```
#### Page（属性）

当前页面 URL。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.ControlCenter1 Page
```
#### Path（属性）

当前页面路径。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.ControlCenter1 Path
```
---
