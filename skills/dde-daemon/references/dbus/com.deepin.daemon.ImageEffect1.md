# com.deepin.daemon.ImageEffect1 接口参考

该接口提供图像效果查询和删除能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `com.deepin.daemon.ImageEffect` |
| Object path | `/com/deepin/daemon/ImageEffect` |
| Interface | `com.deepin.daemon.ImageEffect1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 图像效果方法

#### Get

获取图像效果。

- **输入参数**: `imagePath`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：效果图像路径

```bash
gdbus call --session \
  --dest com.deepin.daemon.ImageEffect \
  --object-path /com/deepin/daemon/ImageEffect \
  --method com.deepin.daemon.ImageEffect1.Get "/path/to/image.png"
```

#### Delete

删除图像效果。

- **输入参数**: `imagePath`（string, 类型 `s`）：图像路径
- **返回值**: 无

```bash
gdbus call --session \
  --dest com.deepin.daemon.ImageEffect \
  --object-path /com/deepin/daemon/ImageEffect \
  --method com.deepin.daemon.ImageEffect1.Delete "/path/to/image.png"
```

