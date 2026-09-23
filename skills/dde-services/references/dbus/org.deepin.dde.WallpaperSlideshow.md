# org.deepin.dde.WallpaperSlideshow 接口参考

该接口提供壁纸轮播配置能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.WallpaperSlideshow` |
| Object path | `/org/deepin/dde/WallpaperSlideshow` |
| Interface | `org.deepin.dde.WallpaperSlideshow` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 壁纸轮播属性

#### WallpaperSlideShow（属性）

壁纸轮播配置 JSON。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | readwrite |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperSlideshow \
  --object-path /org/deepin/dde/WallpaperSlideshow \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.WallpaperSlideshow WallpaperSlideShow
```
设置示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperSlideshow \
  --object-path /org/deepin/dde/WallpaperSlideshow \
  --method org.freedesktop.DBus.Properties.Set \
  org.deepin.dde.WallpaperSlideshow WallpaperSlideShow "<json_string>"
```
---
