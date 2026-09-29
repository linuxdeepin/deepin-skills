# org.deepin.dde.ImageBlur1 兼容性接口概述

该接口为兼容性接口，用于替代 dde-daemon 的 ImageBlur 服务，使旧版应用在 Treeland 会话下仍可正常调用。实际实现挂载在 WallpaperCache 服务上，提供图像模糊处理及模糊完成信号。

> **注意**：此接口为兼容性接口，不建议在新代码中使用。图像模糊处理请使用最新的 `org.deepin.dde.WallpaperCache` 接口替代。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ImageBlur1` |
| Object path | `/org/deepin/dde/ImageBlur1` |
| Interface | `org.deepin.dde.ImageBlur1` |
| Bus | Session |

## 功能概述

- **Get(filename)**：获取模糊后的图像，委托给 WallpaperCache 服务的模糊处理功能
- **Delete(filename)**：删除模糊图像，委托给 WallpaperCache 服务处理
- **BlurDone(file, blurFile, ok)**（信号）：模糊处理完成时发出

> 如需处理图像模糊，建议使用最新的 `org.deepin.dde.WallpaperCache` 接口（`GetBlurImagePath`、`GetProcessedImageWithBlur`、`GetProcessedImagePathByFdWithBlur` 方法），详见 [org.deepin.dde.WallpaperCache.md](org.deepin.dde.WallpaperCache.md)。
