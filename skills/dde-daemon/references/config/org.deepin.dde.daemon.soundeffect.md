# org.deepin.dde.daemon.soundeffect

音效配置资源，控制系统各种事件（音量变化音效、相机快门音效、文件复制完成音效、打印完成音效、桌面登录音效、桌面登出音效、设备添加音效、设备移除音效、错误对话框音效、严重错误对话框音效、重要错误对话框音效、音效总开关、消息通知音效、音效播放器、电源插入音效、电源拔出音效、低电量提示音效、截图开始音效、截图完成音效、系统唤醒音效、系统关机音效、清空回收站音效、应用发送到桌面音效）的提示音开关。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `audio-volume-change` | 音量变化音效 | 控制音量变化时是否播放提示音效 | bool | readwrite |
| `camera-shutter` | 相机快门音效 | 控制拍照时是否播放快门音效 | bool | readwrite |
| `complete-copy` | 文件复制完成音效 | 控制文件复制完成时是否播放提示音效 | bool | readwrite |
| `complete-print` | 打印完成音效 | 控制打印任务完成时是否播放提示音效 | bool | readwrite |
| `desktop-login` | 桌面登录音效 | 控制桌面环境登录时是否播放音效 | bool | readwrite |
| `desktop-logout` | 桌面登出音效 | 控制桌面环境登出时是否播放音效 | bool | readwrite |
| `device-added` | 设备添加音效 | 控制添加可移动设备时是否播放提示音效 | bool | readwrite |
| `device-removed` | 设备移除音效 | 控制移除可移动设备时是否播放提示音效 | bool | readwrite |
| `dialog-error` | 错误对话框音效 | 控制错误对话框弹出时是否播放提示音效 | bool | readwrite |
| `dialog-error-critical` | 严重错误对话框音效 | 控制严重错误对话框弹出时是否播放提示音效 | bool | readwrite |
| `dialog-error-serious` | 重要错误对话框音效 | 控制重要错误对话框弹出时是否播放提示音效 | bool | readwrite |
| `enabled` | 音效总开关 | 控制系统音效功能的总开关，关闭后所有音效均不播放 | bool | readwrite |
| `message` | 消息通知音效 | 控制桌面通知显示时是否播放提示音效 | bool | readwrite |
| `player` | 音效播放器 | 配置音效事件的播放器后端，0 为 libcanberra、1 为 paplay、3 为 mpv | number | readwrite |
| `power-plug` | 电源插入音效 | 控制电源适配器插入时是否播放提示音效 | bool | readwrite |
| `power-unplug` | 电源拔出音效 | 控制电源适配器拔出时是否播放提示音效 | bool | readwrite |
| `power-unplug-battery-low` | 低电量提示音效 | 控制拔出电源且电池电量低时是否播放警告音效 | bool | readwrite |
| `screen-capture` | 截图开始音效 | 控制开始截图时是否播放提示音效 | bool | readwrite |
| `screen-capture-complete` | 截图完成音效 | 控制截图完成时是否播放提示音效 | bool | readwrite |
| `suspend-resume` | 系统唤醒音效 | 控制系统从挂起状态恢复时是否播放音效 | bool | readwrite |
| `system-shutdown` | 系统关机音效 | 控制系统关机时是否播放音效 | bool | readwrite |
| `trash-empty` | 清空回收站音效 | 控制清空回收站时是否播放提示音效 | bool | readwrite |
| `x-deepin-app-sent-to-desktop` | 应用发送到桌面音效 | 控制应用发送到桌面时是否播放提示音效 | bool | readwrite |

## 读写示例

```bash
# 查询音效总开关
dde-dconfig get -a org.deepin.dde.daemon -r org.deepin.dde.daemon.soundeffect -k enabled
# 设置音效总开关
dde-dconfig set -a org.deepin.dde.daemon -r org.deepin.dde.daemon.soundeffect -k enabled -v "<value>"
```
