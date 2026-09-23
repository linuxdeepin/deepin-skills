# org.deepin.customscreensaver

自定义屏保轮播配置资源，管理屏保图片的轮播间隔、播放模式和图片路径。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `intervalTime` | 屏保轮播间隔 | 配置自定义屏保图片轮播切换的时间间隔（范围 3-3600 秒） | number | readwrite |
| `playMode` | 屏保播放模式 | 配置自定义屏保的图片播放模式（顺序播放、随机播放） | number | readwrite |
| `slideshowPath` | 屏保图片路径 | 配置自定义屏保轮播图片的目录路径 | string | readwrite |

## 读写示例

```bash
# 查询轮播间隔
dde-dconfig get -a org.deepin.screensaver -r org.deepin.customscreensaver -k intervalTime
# 设置轮播间隔
dde-dconfig set -a org.deepin.screensaver -r org.deepin.customscreensaver -k intervalTime -v "<value>"
```
