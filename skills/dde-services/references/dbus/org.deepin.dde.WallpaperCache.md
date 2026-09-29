# org.deepin.dde.WallpaperCache 接口参考

该接口提供壁纸缓存能力，包括处理后图像路径获取和模糊处理。壁纸缓存服务负责对原始壁纸图像进行尺寸适配和模糊效果处理，并将处理后的图像缓存供桌面组件使用。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.WallpaperCache` |
| Object path | `/org/deepin/dde/WallpaperCache` |
| Interface | `org.deepin.dde.WallpaperCache` |
| Bus | Session |

### 壁纸缓存查询

#### GetProcessedImagePaths

获取处理后图像路径列表。

- **功能**：根据原始壁纸路径和所需尺寸，返回适配指定尺寸后的处理后图像路径列表
- **触发条件**：桌面壁纸组件需要获取适配屏幕尺寸的壁纸图像时调用
- **输入参数**：`originalPath`（string, 类型 `s`）：原始路径；`sizeArray`（variant 数组, 类型 `av`）：尺寸数组
- **返回值**：`as`（string 数组）：处理后图像路径列表
- **使用场景**：桌面壁纸组件需要获取适配屏幕尺寸的壁纸图像时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperCache \
  --object-path /org/deepin/dde/WallpaperCache \
  --method org.deepin.dde.WallpaperCache.GetProcessedImagePaths "/path/to/wallpaper.jpg" [<variant 1920x1080>]
```

#### GetProcessedImagePathByFd

通过文件描述符获取处理后图像路径。

- **功能**：通过文件描述符传递原始壁纸数据，避免大文件通过 D-Bus 传输，返回适配指定尺寸后的处理后图像路径列表
- **触发条件**：壁纸图像较大时通过文件描述符传递以提高传输效率时调用
- **输入参数**：`fd`（handle, 类型 `h`）：文件描述符；`imagePathMd5`（string, 类型 `s`）：图像路径 MD5；`sizeArray`（variant 数组, 类型 `av`）：尺寸数组
- **返回值**：`as`（string 数组）：处理后图像路径列表
- **使用场景**：壁纸图像较大时，通过文件描述符传递以提高传输效率

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperCache \
  --object-path /org/deepin/dde/WallpaperCache \
  --method org.deepin.dde.WallpaperCache.GetProcessedImagePathByFd <fd> "md5hash" [<variant 1920x1080>]
```

#### GetBlurImagePath

获取模糊图像路径。

- **功能**：根据原始壁纸路径，返回模糊处理后的图像路径
- **触发条件**：锁屏界面或桌面模糊背景需要模糊壁纸时调用
- **输入参数**：`originalPath`（string, 类型 `s`）：原始路径
- **返回值**：`s`（string）：模糊图像路径
- **使用场景**：锁屏界面、桌面模糊背景需要模糊壁纸的场景

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperCache \
  --object-path /org/deepin/dde/WallpaperCache \
  --method org.deepin.dde.WallpaperCache.GetBlurImagePath "/path/to/wallpaper.jpg"
```

#### GetProcessedImageWithBlur

获取带模糊效果的处理后图像。

- **功能**：根据原始壁纸路径和所需尺寸，返回适配尺寸并可选模糊处理后的图像路径列表
- **触发条件**：锁屏界面需要适配尺寸且模糊的壁纸图像时调用
- **输入参数**：`originalPath`（string, 类型 `s`）：原始路径；`sizeArray`（variant 数组, 类型 `av`）：尺寸数组；`needBlur`（bool, 类型 `b`）：是否需要模糊
- **返回值**：`as`（string 数组）：处理后图像路径列表
- **使用场景**：锁屏界面需要适配尺寸且模糊的壁纸图像时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperCache \
  --object-path /org/deepin/dde/WallpaperCache \
  --method org.deepin.dde.WallpaperCache.GetProcessedImageWithBlur "/path/to/wallpaper.jpg" [<variant 1920x1080>] true
```

#### GetProcessedImagePathByFdWithBlur

通过文件描述符获取带模糊效果的处理后图像。

- **功能**：通过文件描述符传递原始壁纸数据，返回适配指定尺寸并可选模糊处理后的图像路径列表
- **触发条件**：壁纸图像较大且需要模糊效果时通过文件描述符传递以提高传输效率时调用
- **输入参数**：`fd`（handle, 类型 `h`）：文件描述符；`imagePathMd5`（string, 类型 `s`）：图像路径 MD5；`sizeArray`（variant 数组, 类型 `av`）：尺寸数组；`needBlur`（bool, 类型 `b`）：是否需要模糊
- **返回值**：`as`（string 数组）：处理后图像路径列表
- **使用场景**：壁纸图像较大且需要模糊效果时，通过文件描述符传递以提高传输效率

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperCache \
  --object-path /org/deepin/dde/WallpaperCache \
  --method org.deepin.dde.WallpaperCache.GetProcessedImagePathByFdWithBlur <fd> "md5hash" [<variant 1920x1080>] true
```

#### GetWallpaperListForScreen

获取屏幕壁纸列表。

- **功能**：根据原始壁纸路径和所需尺寸，返回适配尺寸并可选模糊处理后的壁纸路径列表，专用于屏幕壁纸获取
- **触发条件**：桌面壁纸组件获取当前屏幕所需壁纸图像时调用
- **输入参数**：`originalPath`（string, 类型 `s`）：原始路径；`sizeArray`（variant 数组, 类型 `av`）：尺寸数组；`needBlur`（bool, 类型 `b`）：是否需要模糊
- **返回值**：`as`（string 数组）：壁纸路径列表
- **使用场景**：桌面壁纸组件获取当前屏幕所需壁纸图像时调用

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperCache \
  --object-path /org/deepin/dde/WallpaperCache \
  --method org.deepin.dde.WallpaperCache.GetWallpaperListForScreen "/path/to/wallpaper.jpg" [<variant 1920x1080>] true
```

---
