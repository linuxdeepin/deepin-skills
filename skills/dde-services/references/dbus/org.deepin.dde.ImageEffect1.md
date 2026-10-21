# org.deepin.dde.ImageEffect1 兼容接口说明

该历史接口已废弃，不用于新调用。它保留 图像效果 Get/Delete 的旧协议，由壁纸缓存服务兼容处理；新调用使用 [org.deepin.dde.WallpaperCache](org.deepin.dde.WallpaperCache.md)。

兼容接口与壁纸缓存均处理壁纸派生图像，不替代通用图像裁剪、缩放或格式转换能力。旧调用方迁移时需使用壁纸缓存的参数、结果与缓存语义，不能只替换接口名称。
