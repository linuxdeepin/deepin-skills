# org.deepin.dde.ImageEffect1 接口参考

> **已废弃/不推荐使用**：该接口为兼容性接口，用于替代 dde-daemon 的 ImageEffect 服务，使旧版应用在 Treeland 会话下仍可正常调用。实际实现挂载在 WallpaperCache 服务上，仅支持 "pixmix"/blur 效果。新代码请使用 `org.deepin.dde.WallpaperCache` 接口替代。

该接口提供图像效果处理能力，支持获取和删除指定效果的图像。实际实现委托给 WallpaperCache 服务处理。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ImageEffect1` |
| Object path | `/org/deepin/dde/ImageEffect1` |
| Interface | `org.deepin.dde.ImageEffect1` |
| Bus | Session |

### 图像效果

#### Get

获取指定效果的图像。

- **功能**：根据效果名称和原始文件名，返回经过指定效果处理后的图像路径
- **触发条件**：桌面组件需要获取特效处理后的壁纸图像时调用
- **输入参数**：`effect`（string, 类型 `s`）：效果名称；`filename`（string, 类型 `s`）：文件名
- **返回值**：`s`（string）：处理后的图像路径
- **使用场景**：需要效果处理的场景，如桌面背景特效、锁屏模糊

```bash
gdbus call --session \
  --dest org.deepin.dde.ImageEffect1 \
  --object-path /org/deepin/dde/ImageEffect1 \
  --method org.deepin.dde.ImageEffect1.Get "blur" "wallpaper.jpg"
```

#### Delete

删除指定效果的图像。

- **功能**：根据效果名称和原始文件名，删除对应的特效缓存图像
- **触发条件**：壁纸更换或清理特效缓存时调用
- **输入参数**：`effect`（string, 类型 `s`）：效果名称；`filename`（string, 类型 `s`）：文件名
- **返回值**：无
- **使用场景**：壁纸更换后清理旧特效缓存、系统缓存清理

```bash
gdbus call --session \
  --dest org.deepin.dde.ImageEffect1 \
  --object-path /org/deepin/dde/ImageEffect1 \
  --method org.deepin.dde.ImageEffect1.Delete "blur" "wallpaper.jpg"
```

---
