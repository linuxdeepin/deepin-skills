# org.freedesktop.portal.Desktop

服务位于当前用户的 Session 总线，服务名为 `org.freedesktop.portal.Desktop`，对象路径为 `/org/freedesktop/portal/desktop`。前端实际暴露的接口由部署版本和后端配置决定，后端协议的存在不表示前端已提供相应能力。

接口查看示例：

```bash
busctl --user introspect org.freedesktop.portal.Desktop /org/freedesktop/portal/desktop
```

## Settings：外观设置与配色方案

`org.freedesktop.portal.Settings.ReadAll(as)` 枚举指定命名空间中的设置。返回类型为 `a{sa{sv}}`，外层键是命名空间，内层键是设置名。

```bash
gdbus call --session \
  --dest org.freedesktop.portal.Desktop \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.portal.Settings.ReadAll "['org.freedesktop.appearance']"
```

`ReadOne(ss)` 读取命名空间下的单项设置；旧版本提供 `Read(ss)`。可用方法及 variant 的封装以当前前端接口为准。

```bash
gdbus call --session \
  --dest org.freedesktop.portal.Desktop \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.portal.Settings.ReadOne org.freedesktop.appearance color-scheme
```

`color-scheme` 的无符号整数含义：0 为无偏好，1 为偏好深色，2 为偏好浅色。此值表示门户返回的配色偏好，与 GTK 主题名称或 Appearance1 的设置属于不同状态来源。`ReadAll` 的空集合、未返回目标命名空间、单项设置缺失和服务错误具有不同含义，均不等同于 `color-scheme=0`。

## GlobalShortcuts：接口与版本

`org.freedesktop.portal.GlobalShortcuts` 提供应用全局快捷键能力，`version` 属性表示接口版本。属性读取不创建快捷键会话；`CreateSession` 和 `BindShortcuts` 属于会话及绑定操作。

```bash
busctl --user get-property org.freedesktop.portal.Desktop \
  /org/freedesktop/portal/desktop org.freedesktop.portal.GlobalShortcuts version
```

前端未暴露该接口表示当前部署不提供此入口；前端探测失败无法确定接口是否存在。DDE 的 `org.deepin.dde.Keybinding1` 管理桌面快捷键，与 Portal GlobalShortcuts 的应用接口具有不同用途。`org.freedesktop.impl.portal.*` 是前后端协作协议。

## Account、Background 与 Notification

`Account` 提供用户信息请求，`Background` 提供后台运行相关能力，`Notification` 提供门户通知的发送和撤回。接口可用性及签名取决于前端与后端部署；账户服务和桌面通知服务是不同的接口入口。

- `org.freedesktop.portal.Account.GetUserInformation`：签名为 `sa{sv} → o`，返回请求对象路径；用户信息及完成、取消或失败状态通过请求的 `Response` 信号返回。首个字符串参数为父窗口标识，与应用 ID 含义不同；应用身份由门户识别。
- `org.freedesktop.portal.Background`：提供后台运行相关能力；接口发现与后台运行授权请求、自启动配置是不同操作。
- `org.freedesktop.portal.Notification`：`AddNotification` 签名为 `sa{sv}`，`RemoveNotification` 为 `s`；通知字典包含通知内容，撤回操作通过同一调用方身份和通知 ID 定位通知。接口探测不产生通知，`AddNotification` 会实际发送通知。

接口签名与可用性以目标部署为准。introspect 仅提供接口元信息，不表示 Account 请求或通知交互已完成。
