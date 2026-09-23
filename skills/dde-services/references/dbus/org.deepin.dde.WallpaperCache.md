# org.deepin.dde.WallpaperCache 接口参考

该接口提供壁纸缓存能力，包括处理后图像路径获取和模糊处理。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.WallpaperCache` |
| Object path | `/org/deepin/dde/WallpaperCache` |
| Interface | `org.deepin.dde.WallpaperCache` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 壁纸缓存查询

#### GetProcessedImagePaths

获取处理后图像路径列表。

- **输入参数**: `originalPath`（string, 类型 `s`）：原始路径；`sizeArray`（variant 数组, 类型 `av`）：尺寸数组
- **返回值**: `as`（string 数组）：处理后图像路径列表

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperCache \
  --object-path /org/deepin/dde/WallpaperCache \
  --method org.deepin.dde.WallpaperCache.GetProcessedImagePaths "/path/to/wallpaper.jpg" [<variant 1920x1080>]
```

#### GetProcessedImagePathByFd

通过文件描述符获取处理后图像路径。

- **输入参数**: `fd`（handle, 类型 `h`）：文件描述符；`imagePathMd5`（string, 类型 `s`）：图像路径 MD5；`sizeArray`（variant 数组, 类型 `av`）：尺寸数组
- **返回值**: `as`（string 数组）：处理后图像路径列表

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperCache \
  --object-path /org/deepin/dde/WallpaperCache \
  --method org.deepin.dde.WallpaperCache.GetProcessedImagePathByFd <fd> "md5hash" [<variant 1920x1080>]
```

#### GetBlurImagePath

获取模糊图像路径。

- **输入参数**: `originalPath`（string, 类型 `s`）：原始路径
- **返回值**: `s`（string）：模糊图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperCache \
  --object-path /org/deepin/dde/WallpaperCache \
  --method org.deepin.dde.WallpaperCache.GetBlurImagePath "/path/to/wallpaper.jpg"
```

#### GetProcessedImageWithBlur

获取带模糊效果的处理后图像。

- **输入参数**: `originalPath`（string, 类型 `s`）：原始路径；`sizeArray`（variant 数组, 类型 `av`）：尺寸数组；`needBlur`（bool, 类型 `b`）：是否需要模糊
- **返回值**: `as`（string 数组）：处理后图像路径列表

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperCache \
  --object-path /org/deepin/dde/WallpaperCache \
  --method org.deepin.dde.WallpaperCache.GetProcessedImageWithBlur "/path/to/wallpaper.jpg" [<variant 1920x1080>] true
```

#### GetProcessedImagePathByFdWithBlur

通过文件描述符获取带模糊效果的处理后图像。

- **输入参数**: `fd`（handle, 类型 `h`）：文件描述符；`imagePathMd5`（string, 类型 `s`）：图像路径 MD5；`sizeArray`（variant 数组, 类型 `av`）：尺寸数组；`needBlur`（bool, 类型 `b`）：是否需要模糊
- **返回值**: `as`（string 数组）：处理后图像路径列表

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperCache \
  --object-path /org/deepin/dde/WallpaperCache \
  --method org.deepin.dde.WallpaperCache.GetProcessedImagePathByFdWithBlur <fd> "md5hash" [<variant 1920x1080>] true
```

#### GetWallpaperListForScreen

获取屏幕壁纸列表。

- **输入参数**: `originalPath`（string, 类型 `s`）：原始路径；`sizeArray`（variant 数组, 类型 `av`）：尺寸数组；`needBlur`（bool, 类型 `b`）：是否需要模糊
- **返回值**: `as`（string 数组）：壁纸路径列表

```bash
gdbus call --session \
  --dest org.deepin.dde.WallpaperCache \
  --object-path /org/deepin/dde/WallpaperCache \
  --method org.deepin.dde.WallpaperCache.GetWallpaperListForScreen "/path/to/wallpaper.jpg" [<variant 1920x1080>] true
```

---
