# org.deepin.dde.Graphic1 接口参考

该接口提供图像模糊、裁剪、格式转换、合成、翻转、旋转、缩放、缩略图生成和颜色空间转换能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Graphic1` |
| Object path | `/org/deepin/dde/Graphic1` |
| Interface | `org.deepin.dde.Graphic1` |
| Bus | Session |


### 图像模糊

#### BlurImage

对图像进行高斯模糊处理。

- **输入参数**: `srcFile`（string, 类型 `s`）：源图像路径；`dstFile`（string, 类型 `s`）：目标图像路径；`sigma`（double, 类型 `d`）：模糊强度；`numSteps`（double, 类型 `d`）：模糊步数；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.BlurImage \
  "/path/to/input.png" "/path/to/output.png" 20.0 10.0 "png"
```


### 图像裁剪

#### ClipImage

裁剪图像的指定区域。

- **输入参数**: `srcFile`（string, 类型 `s`）：源图像路径；`dstFile`（string, 类型 `s`）：目标图像路径；`x`（int32, 类型 `i`）：裁剪起始 X 坐标；`y`（int32, 类型 `i`）：裁剪起始 Y 坐标；`w`（int32, 类型 `i`）：裁剪宽度；`h`（int32, 类型 `i`）：裁剪高度；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.ClipImage \
  "/path/to/input.png" "/path/to/output.png" 0 0 100 100 "png"
```


### 图像格式转换

#### ConvertImage

将图像从一种格式转换为另一种格式。

- **输入参数**: `srcFile`（string, 类型 `s`）：源图像路径；`dstFile`（string, 类型 `s`）：目标图像路径；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.ConvertImage \
  "/path/to/input.bmp" "/path/to/output.png" "png"
```

#### ConvertImageToDataUri

将图像文件转换为 Data URI 格式。

- **输入参数**: `imgfile`（string, 类型 `s`）：图像文件路径
- **返回值**: `dataUri`（string, 类型 `s`）：Data URI 字符串

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.ConvertImageToDataUri \
  "/path/to/input.png"
```

#### ConvertDataUriToImage

将 Data URI 转换为图像文件。

- **输入参数**: `dataUri`（string, 类型 `s`）：Data URI 字符串；`dstFile`（string, 类型 `s`）：目标图像路径；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.ConvertDataUriToImage \
  "data:image/png;base64,iVBOR..." "/path/to/output.png" "png"
```


### 图像合成

#### CompositeImage

将两张图像合成为一张。

- **输入参数**: `srcFile`（string, 类型 `s`）：源图像路径；`compFile`（string, 类型 `s`）：叠加图像路径；`dstFile`（string, 类型 `s`）：目标图像路径；`x`（int32, 类型 `i`）：叠加起始 X 坐标；`y`（int32, 类型 `i`）：叠加起始 Y 坐标；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.CompositeImage \
  "/path/to/background.png" "/path/to/overlay.png" "/path/to/output.png" 10 10 "png"
```

#### CompositeImageUri

将两个 Data URI 格式的图像合成为一张，返回 Data URI。

- **输入参数**: `srcDataUri`（string, 类型 `s`）：源图像 Data URI；`compDataUri`（string, 类型 `s`）：叠加图像 Data URI；`x`（int32, 类型 `i`）：叠加起始 X 坐标；`y`（int32, 类型 `i`）：叠加起始 Y 坐标；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: `resultDataUri`（string, 类型 `s`）：合成结果的 Data URI

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.CompositeImageUri \
  "data:image/png;base64,AAAA..." "data:image/png;base64,BBBB..." 10 10 "png"
```


### 颜色处理

#### GetDominantColorOfImage

获取图像的主色调（HSV 格式）。

- **输入参数**: `imgFile`（string, 类型 `s`）：图像文件路径
- **返回值**: `h`（double, 类型 `d`）：色相；`s`（double, 类型 `d`）：饱和度；`v`（double, 类型 `d`）：明度

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.GetDominantColorOfImage \
  "/path/to/input.png"
```

#### Rgb2Hsv

将 RGB 颜色转换为 HSV 颜色。

- **输入参数**: `r`（byte, 类型 `y`）：红色分量（0-255）；`g`（byte, 类型 `y`）：绿色分量（0-255）；`b`（byte, 类型 `y`）：蓝色分量（0-255）
- **返回值**: `h`（double, 类型 `d`）：色相（0-360）；`s`（double, 类型 `d`）：饱和度（0-1）；`v`（double, 类型 `d`）：明度（0-1）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Rgb2Hsv 255 0 0
```

#### Hsv2Rgb

将 HSV 颜色转换为 RGB 颜色。

- **输入参数**: `h`（double, 类型 `d`）：色相（0-360）；`s`（double, 类型 `d`）：饱和度（0-1）；`v`（double, 类型 `d`）：明度（0-1）
- **返回值**: `r`（byte, 类型 `y`）：红色分量（0-255）；`g`（byte, 类型 `y`）：绿色分量（0-255）；`b`（byte, 类型 `y`）：蓝色分量（0-255）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Hsv2Rgb 0.0 1.0 1.0
```


### 图像填充

#### FillImage

通过源图像生成指定宽高的新图像，支持多种填充样式。

- **输入参数**: `srcFile`（string, 类型 `s`）：源图像路径；`dstFile`（string, 类型 `s`）：目标图像路径；`width`（int32, 类型 `i`）：目标宽度；`height`（int32, 类型 `i`）：目标高度；`style`（string, 类型 `s`）：填充样式（`tile` 或 `center`）；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.FillImage \
  "/path/to/input.png" "/path/to/output.png" 1920 1080 "center" "png"
```


### 图像翻转

#### FlipImageHorizontal

水平翻转图像。

- **输入参数**: `srcFile`（string, 类型 `s`）：源图像路径；`dstFile`（string, 类型 `s`）：目标图像路径；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.FlipImageHorizontal \
  "/path/to/input.png" "/path/to/output.png" "png"
```

#### FlipImageVertical

垂直翻转图像。

- **输入参数**: `srcFile`（string, 类型 `s`）：源图像路径；`dstFile`（string, 类型 `s`）：目标图像路径；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.FlipImageVertical \
  "/path/to/input.png" "/path/to/output.png" "png"
```


### 图像尺寸

#### GetImageSize

获取图像的宽度和高度。

- **输入参数**: `imgFile`（string, 类型 `s`）：图像文件路径
- **返回值**: `width`（int32, 类型 `i`）：图像宽度；`height`（int32, 类型 `i`）：图像高度

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.GetImageSize \
  "/path/to/input.png"
```


### 图像缩放

#### ResizeImage

将图像缩放到指定宽高。

- **输入参数**: `srcFile`（string, 类型 `s`）：源图像路径；`dstFile`（string, 类型 `s`）：目标图像路径；`newWidth`（int32, 类型 `i`）：目标宽度；`newHeight`（int32, 类型 `i`）：目标高度；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.ResizeImage \
  "/path/to/input.png" "/path/to/output.png" 800 600 "png"
```

#### ThumbnailImage

按最大宽高限制生成缩略图。

- **输入参数**: `srcFile`（string, 类型 `s`）：源图像路径；`dstFile`（string, 类型 `s`）：目标图像路径；`maxWidth`（uint32, 类型 `u`）：最大宽度；`maxHeight`（uint32, 类型 `u`）：最大高度；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.ThumbnailImage \
  "/path/to/input.png" "/path/to/output.png" 200 200 "png"
```


### 图像旋转

#### RotateImageLeft

将图像向左旋转 90 度。

- **输入参数**: `srcFile`（string, 类型 `s`）：源图像路径；`dstFile`（string, 类型 `s`）：目标图像路径；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.RotateImageLeft \
  "/path/to/input.png" "/path/to/output.png" "png"
```

#### RotateImageRight

将图像向右旋转 90 度。

- **输入参数**: `srcFile`（string, 类型 `s`）：源图像路径；`dstFile`（string, 类型 `s`）：目标图像路径；`format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.RotateImageRight \
  "/path/to/input.png" "/path/to/output.png" "png"
```

---
