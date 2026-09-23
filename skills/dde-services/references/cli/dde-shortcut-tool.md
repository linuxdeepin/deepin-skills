# dde-shortcut-tool 命令参考

DDE 快捷键工具，通过子命令 + action 模式执行各类系统快捷操作。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-services` |
| 安装路径 | `/usr/bin/dde-shortcut-tool` |
| DDE 角色 | 系统调用的辅助工具，由快捷键守护进程自动调用执行 |

## 用途

DDE 快捷键工具，通过子命令 + action 模式执行各类系统快捷操作。它是 DDE 快捷键系统的后端执行器，当用户按下键盘快捷键时，系统会调用此工具来执行对应的操作。覆盖的功能领域包括：音频控制（静音切换、音量调节、麦克风静音）、显示控制（亮度调节、显示模式切换、关屏）、触摸板控制（开关切换）、电源管理（电源按钮、模式切换、休眠）、键盘背光控制、媒体播放控制（播放/暂停/上一首/下一首）、锁定键控制（CapsLock/NumLock）、应用启动、网络控制（WiFi/飞行模式切换）、窗口管理器特效切换、摄像头控制。该工具是系统级工具，通常由快捷键守护进程调用，一般不需要用户直接运行。

## 用法

`dde-shortcut-tool <command> <action> [options]`

## 全局选项

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |

## 子命令及 Actions

| 子命令 | 说明 | Actions |
|--------|------|---------|
| `audio` | 音频控制 | `mute-toggle`、`volume-up`、`volume-down`、`mic-mute-toggle` |
| `display` | 显示控制 | `brightness-up`、`brightness-down`、`switch-mode`、`turn-off-screen` |
| `touchpad` | 触摸板控制 | `toggle`、`on`、`off` |
| `power` | 电源控制 | `button`、`switch-mode`、`system-away`、`show-ui` |
| `kbdlight` | 键盘背光控制 | `toggle`、`brightness-up`、`brightness-down` |
| `media` | 媒体播放控制 | `play`、`play-pause`、`pause`、`stop`、`previous`、`next`、`rewind`、`forward` |
| `lockkey` | 锁定键控制 | `capslock`、`numlock` |
| `launch` | 启动应用 | `mime` |
| `network` | 网络控制 | `toggle-wifi`、`toggle-airplane` |
| `wm` | 窗口管理器控制 | `switch-effects` |
| `camera` | 摄像头控制 | `toggle`、`on`、`off` |

## 使用示例

```bash
# --- 音频控制 ---
# 切换静音状态
dde-shortcut-tool audio mute-toggle

# 音量增加
dde-shortcut-tool audio volume-up

# 音量减少
dde-shortcut-tool audio volume-down

# 切换麦克风静音
dde-shortcut-tool audio mic-mute-toggle

# --- 显示控制 ---
# 屏幕亮度增加
dde-shortcut-tool display brightness-up

# 屏幕亮度减少
dde-shortcut-tool display brightness-down

# 切换显示模式（如镜像/扩展）
dde-shortcut-tool display switch-mode

# 关闭屏幕
dde-shortcut-tool display turn-off-screen

# --- 触摸板控制 ---
# 切换触摸板开关
dde-shortcut-tool touchpad toggle

# 开启触摸板
dde-shortcut-tool touchpad on

# 关闭触摸板
dde-shortcut-tool touchpad off

# --- 电源控制 ---
# 电源按钮动作
dde-shortcut-tool power button

# 切换电源模式
dde-shortcut-tool power switch-mode

# 系统休眠
dde-shortcut-tool power system-away

# 显示电源 UI
dde-shortcut-tool power show-ui

# --- 键盘背光控制 ---
# 切换键盘背光
dde-shortcut-tool kbdlight toggle

# 键盘背光亮度增加
dde-shortcut-tool kbdlight brightness-up

# 键盘背光亮度减少
dde-shortcut-tool kbdlight brightness-down

# --- 媒体播放控制 ---
# 播放/暂停切换
dde-shortcut-tool media play-pause

# 上一首
dde-shortcut-tool media previous

# 下一首
dde-shortcut-tool media next

# 停止播放
dde-shortcut-tool media stop

# 快退
dde-shortcut-tool media rewind

# 快进
dde-shortcut-tool media forward

# --- 锁定键控制 ---
# 切换 CapsLock
dde-shortcut-tool lockkey capslock

# 切换 NumLock
dde-shortcut-tool lockkey numlock

# --- 应用启动 ---
# 通过 MIME 类型启动关联应用
dde-shortcut-tool launch mime

# --- 网络控制 ---
# 切换 WiFi 开关
dde-shortcut-tool network toggle-wifi

# 切换飞行模式
dde-shortcut-tool network toggle-airplane

# --- 窗口管理器控制 ---
# 切换窗口管理器特效
dde-shortcut-tool wm switch-effects

# --- 摄像头控制 ---
# 切换摄像头开关
dde-shortcut-tool camera toggle

# 开启摄像头
dde-shortcut-tool camera on

# 关闭摄像头
dde-shortcut-tool camera off
```
