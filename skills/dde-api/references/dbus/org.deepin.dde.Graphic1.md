# org.deepin.dde.Graphic1 接口参考

该接口提供图像裁剪、缩放、旋转、模糊、圆角处理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Graphic1` |
| Object path | `/org/deepin/dde/Graphic1` |
| Interface | `org.deepin.dde.Graphic1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 图像处理方法

#### BGR2RGB

将 BGR 图像转换为 RGB。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.BGR2RGB "/path/to/image.png"
```

#### BlurImage

对图像进行模糊处理。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.BlurImage "/path/to/image.png"
```

#### CornerImage

对图像进行圆角处理。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.CornerImage "/path/to/image.png"
```

#### CropImage

裁剪图像。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.CropImage "/path/to/image.png"
```

#### DeepenColor

加深图像颜色。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.DeepenColor "/path/to/image.png"
```

#### GrayScale

将图像转为灰度。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.GrayScale "/path/to/image.png"
```

#### Resize

调整图像尺寸。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Resize "/path/to/image.png"
```

#### Rotate

旋转图像。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Rotate "/path/to/image.png"
```

#### Saturation

调整图像饱和度。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Saturation "/path/to/image.png"
```

#### Scale

缩放图像。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Scale "/path/to/image.png"
```

#### Fit

适配图像。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Fit "/path/to/image.png"
```

#### Crop

裁剪图像。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Crop "/path/to/image.png"
```

#### FlipH

水平翻转图像。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.FlipH "/path/to/image.png"
```

#### FlipV

垂直翻转图像。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.FlipV "/path/to/image.png"
```

#### Blur

模糊图像。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Blur "/path/to/image.png"
```

#### Round

圆角处理图像。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Round "/path/to/image.png"
```

#### Cover

覆盖处理图像。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Cover "/path/to/image.png"
```

#### Cut

切割图像。

- **输入参数**: `image`（string, 类型 `s`）：图像路径
- **返回值**: `s`（string）：处理后的图像路径

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Cut "/path/to/image.png"
```

