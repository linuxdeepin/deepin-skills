# org.deepin.dde.ImageBlur1 接口参考

> **已废弃/不推荐使用**：该接口为兼容性接口，用于替代 dde-daemon 的 ImageBlur 服务，使旧版应用在 Treeland 会话下仍可正常调用。实际实现挂载在 WallpaperCache 服务上。新代码请使用 `org.deepin.dde.WallpaperCache` 接口替代。

该接口提供图像模糊处理能力，包括获取模糊图像、删除模糊图像以及模糊完成信号。实际实现委托给 WallpaperCache 服务的模糊处理功能。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ImageBlur1` |
| Object path | `/org/deepin/dde/ImageBlur1` |
| Interface | `org.deepin.dde.ImageBlur1` |
| Bus | Session |

### 图像模糊

#### Get

获取模糊后的图像。

- **功能**：根据原始壁纸文件名，返回模糊处理后的图像路径
- **触发条件**：桌面组件需要获取模糊壁纸图像时调用
- **输入参数**：`filename`（string, 类型 `s`）：文件名
- **返回值**：`s`（string）：模糊图像路径
- **使用场景**：需要模糊壁纸的场景，如锁屏界面、桌面模糊背景

```bash
gdbus call --session \
  --dest org.deepin.dde.ImageBlur1 \
  --object-path /org/deepin/dde/ImageBlur1 \
  --method org.deepin.dde.ImageBlur1.Get "wallpaper.jpg"
```

#### Delete

删除模糊图像。

- **功能**：根据原始壁纸文件名，删除对应的模糊缓存图像
- **触发条件**：壁纸更换或清理缓存时调用
- **输入参数**：`filename`（string, 类型 `s`）：文件名
- **返回值**：无
- **使用场景**：壁纸更换后清理旧模糊缓存、系统缓存清理

```bash
gdbus call --session \
  --dest org.deepin.dde.ImageBlur1 \
  --object-path /org/deepin/dde/ImageBlur1 \
  --method org.deepin.dde.ImageBlur1.Delete "wallpaper.jpg"
```

### 模糊信号

#### BlurDone

模糊处理完成时发出。

- **功能**：通知调用方模糊处理已完成，返回处理结果
- **触发条件**：模糊处理完成时发出
- **参数**：`file`（string, 类型 `s`）：原文件名；`blurFile`（string, 类型 `s`）：模糊文件名；`ok`（bool, 类型 `b`）：是否成功
- **使用场景**：调用方异步等待模糊处理完成的场景

```bash
gdbus monitor --session \
  --dest org.deepin.dde.ImageBlur1 \
  --object-path /org/deepin/dde/ImageBlur1
```

---
