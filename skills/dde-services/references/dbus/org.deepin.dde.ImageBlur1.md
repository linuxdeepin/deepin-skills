# org.deepin.dde.ImageBlur1 接口参考

该接口提供图像模糊处理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ImageBlur1` |
| Object path | `/org/deepin/dde/ImageBlur1` |
| Interface | `org.deepin.dde.ImageBlur1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 图像模糊

#### Get

获取模糊后的图像。

- **输入参数**: `filename`（string, 类型 `s`）：文件名
- **返回值**: `s`（string）：模糊图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.ImageBlur1 \
  --object-path /org/deepin/dde/ImageBlur1 \
  --method org.deepin.dde.ImageBlur1.Get "wallpaper.jpg"
```

#### Delete

删除模糊图像。

- **输入参数**: `filename`（string, 类型 `s`）：文件名
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.ImageBlur1 \
  --object-path /org/deepin/dde/ImageBlur1 \
  --method org.deepin.dde.ImageBlur1.Delete "wallpaper.jpg"
```


### 模糊信号

#### BlurDone

模糊处理完成时发出。

- **参数**: `file`（string, 类型 `s`）：原文件名；`blurFile`（string, 类型 `s`）：模糊文件名；`ok`（bool, 类型 `b`）：是否成功
- **触发条件**: 模糊处理完成时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.ImageBlur1 \
  --object-path /org/deepin/dde/ImageBlur1
```

---
