# org.deepin.dde.ControlCenter1 接口参考

该接口在 Session 总线上注册，对象路径为 `/org/deepin/dde/ControlCenter1`，提供控制中心窗口的显示、隐藏、切换、退出、页面跳转和模块列表获取能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ControlCenter1` |
| Object path | `/org/deepin/dde/ControlCenter1` |
| Interface | `org.deepin.dde.ControlCenter1` |
| Bus | Session |

### 窗口显示控制

#### Show

显示控制中心窗口。

- **功能**: 将控制中心窗口显示到桌面前台。
- **触发条件**: 当外部程序需要弹出控制中心界面时调用。
- **使用场景**: dde-shell 面板中的控制中心按钮被点击时，通过 D-Bus 调用此方法显示控制中心。
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

- **功能**: 将控制中心窗口隐藏到后台，不退出进程。
- **触发条件**: 当外部程序需要隐藏控制中心界面时调用。
- **使用场景**: 用户点击桌面空白区域或切换到其他窗口时，dde-shell 调用此方法隐藏控制中心。
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

- **功能**: 若控制中心窗口当前可见则隐藏，若隐藏则显示。
- **触发条件**: 当外部程序需要切换控制中心可见性时调用。
- **使用场景**: dde-shell 面板中的控制中心按钮被再次点击时，通过 D-Bus 调用此方法切换显示状态。
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

- **功能**: 关闭控制中心进程，释放窗口和资源。
- **触发条件**: 当需要彻底关闭控制中心应用时调用。
- **使用场景**: 系统注销或会话结束时，会话管理器调用此方法退出控制中心。
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

- **功能**: 将控制中心切换到首页并显示窗口。
- **触发条件**: 当外部程序需要打开控制中心首页时调用。
- **使用场景**: 用户从某设置页面返回首页，或外部程序需要打开控制中心主界面时调用。
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

- **功能**: 根据页面 URL 导航到控制中心内对应的设置页面，并显示控制中心窗口。
- **触发条件**: 当外部程序需要打开特定设置页面时调用。
- **使用场景**: 通知中心点击"声音设置"跳转到声音页面，或键盘布局提示跳转到键盘设置页面。
- **输入参数**: `url`（string, 类型 `s`）：页面 URL
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.ShowPage "display"
```

#### GetAllModule

获取所有模块信息。

- **功能**: 返回控制中心当前可用的所有设置模块的 JSON 信息，包含模块 ID、名称、图标路径。
- **触发条件**: 当外部程序需要获取控制中心模块列表时调用。
- **使用场景**: dde-shell 或搜索服务需要展示控制中心包含哪些设置模块时调用，用于模块列表展示或全局搜索索引构建。
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

- **功能**: 返回控制中心窗口的位置和尺寸，格式为 `(x, y, width, height)`。
- **触发条件**: 外部程序读取此属性获取窗口位置和尺寸。
- **使用场景**: dde-shell 需要根据控制中心窗口位置调整面板布局，或验证控制中心是否在预期位置显示。
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

- **功能**: 返回控制中心当前显示的设置页面 URL。
- **触发条件**: 外部程序读取此属性获取当前页面。
- **使用场景**: dde-shell 需要根据控制中心当前页面决定是否高亮控制中心按钮，或搜索服务需要判断用户所在页面。
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

- **功能**: 返回控制中心当前页面的层级路径。
- **触发条件**: 外部程序读取此属性获取当前页面层级路径。
- **使用场景**: 外部程序需要判断用户是否在子页面（如显示设置下的缩放子页面）时读取此属性。
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

## 兼容性接口（已废弃/不推荐使用）

控制中心 D-Bus 服务在同一对象 `/org/deepin/dde/ControlCenter1` 上注册了以下已废弃的兼容性方法，保留用于向后兼容旧版调用方。新代码应使用推荐替代方法。

### 旧版服务名 com.deepin.dde.ControlCenter（已废弃/不推荐使用）

除上述方法级兼容外，系统中还存在旧版 D-Bus 服务名 `com.deepin.dde.ControlCenter`，通过 `dde-api-dbus-proxy-v1` 代理转发到新版服务 `org.deepin.dde.ControlCenter1`。旧版服务名仅供向后兼容使用，推荐直接使用新版服务名 `org.deepin.dde.ControlCenter1`，以获得完整的接口能力和更直接的调用路径，避免代理层带来的额外开销。

#### ShowPage(QString module, QString page)（已废弃/不推荐使用）

- **功能**: 旧版双参数页面跳转接口，通过模块名和页面名定位目标页面。已废弃，内部委托给 `ShowPage(QString url)`。
- **推荐替代**: `ShowPage(QString url)`
- **触发条件**: 旧版调用方需要通过模块名+页面名跳转时调用。
- **输入参数**: `module`（string），`page`（string）
- **返回值**: 无

#### ShowModule(QString module)（已废弃/不推荐使用）

- **功能**: 旧版模块显示接口，通过模块名显示指定模块。已废弃，内部委托给 `ShowPage(QString url)`。
- **推荐替代**: `ShowPage(QString url)`
- **触发条件**: 旧版调用方需要通过模块名显示模块时调用。
- **输入参数**: `module`（string）
- **返回值**: 无

以上方法仅为兼容旧版调用方保留，不建议在新代码中使用。
