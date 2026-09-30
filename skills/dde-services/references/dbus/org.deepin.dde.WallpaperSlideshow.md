# org.deepin.dde.WallpaperSlideshow 接口参考

该接口提供壁纸轮播配置能力，用于管理壁纸自动轮播的设置。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.WallpaperSlideshow` |
| Object path | `/org/deepin/dde/WallpaperSlideshow` |
| Interface | `org.deepin.dde.WallpaperSlideshow` |
| Bus | Session |

### 壁纸轮播属性

#### WallpaperSlideShow（属性）

壁纸轮播配置 JSON。

- **功能**：以 JSON 字符串形式存储壁纸轮播的配置信息，包括轮播间隔、壁纸目录、是否启用轮播
- **触发条件**：用户在控制中心修改壁纸轮播设置时更新
- **使用场景**：桌面壁纸组件读取此属性以执行壁纸轮播逻辑

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
