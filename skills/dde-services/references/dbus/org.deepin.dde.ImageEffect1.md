# org.deepin.dde.ImageEffect1 兼容性接口概述

该接口为兼容性接口，用于替代 dde-daemon 的 ImageEffect 服务，使旧版应用在 Treeland 会话下仍可正常调用。实际实现挂载在 WallpaperCache 服务上，仅支持 "pixmix"/blur 效果。

> **注意**：此接口为兼容性接口，不建议在新代码中使用。图像效果处理请使用最新的 `org.deepin.dde.WallpaperCache` 接口替代。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ImageEffect1` |
| Object path | `/org/deepin/dde/ImageEffect1` |
| Interface | `org.deepin.dde.ImageEffect1` |
| Bus | Session |

## 功能概述

- **Get(effect, filename)**：获取指定效果的图像，委托给 WallpaperCache 服务处理
- **Delete(effect, filename)**：删除指定效果的图像，委托给 WallpaperCache 服务处理

> 如需处理图像效果，建议使用最新的 `org.deepin.dde.WallpaperCache` 接口，详见 [org.deepin.dde.WallpaperCache.md](org.deepin.dde.WallpaperCache.md)。
