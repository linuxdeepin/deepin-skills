# org.deepin.dde.ImageEffect1 接口参考

该接口提供图像效果处理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ImageEffect1` |
| Object path | `/org/deepin/dde/ImageEffect1` |
| Interface | `org.deepin.dde.ImageEffect1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 图像效果

#### Get

获取指定效果的图像。

- **输入参数**: `effect`（string, 类型 `s`）：效果名称；`filename`（string, 类型 `s`）：文件名
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.ImageEffect1 \
  --object-path /org/deepin/dde/ImageEffect1 \
  --method org.deepin.dde.ImageEffect1.Get "blur" "wallpaper.jpg"
```

#### Delete

删除指定效果的图像。

- **输入参数**: `effect`（string, 类型 `s`）：效果名称；`filename`（string, 类型 `s`）：文件名
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ImageEffect1 \
  --object-path /org/deepin/dde/ImageEffect1 \
  --method org.deepin.dde.ImageEffect1.Delete "blur" "wallpaper.jpg"
```

---
