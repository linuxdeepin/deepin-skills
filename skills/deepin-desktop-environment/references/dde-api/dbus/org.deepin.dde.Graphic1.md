# org.deepin.dde.Graphic1 接口参考

该接口提供图像模糊、裁剪、合成、格式转换、填充、翻转、缩放、旋转、缩略图生成、主色调提取、尺寸获取、颜色转换能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Graphic1` |
| Object path | `/org/deepin/dde/Graphic1` |
| Interface | `org.deepin.dde.Graphic1` |
| Bus | Session |

## 图像处理方法

### BlurImage

对图像进行高斯模糊处理。

- **功能**: 对指定图像应用高斯模糊算法，生成模糊后的图像文件
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 锁屏壁纸模糊、控制中心毛玻璃背景效果

- **输入参数**:
  - `srcFile`（string, 类型 `s`）：源图像路径
  - `dstFile`（string, 类型 `s`）：目标图像路径
  - `sigma`（double, 类型 `d`）：高斯模糊的 sigma 值
  - `numSteps`（double, 类型 `d`）：模糊步数
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.BlurImage \
  "/path/to/input.png" "/path/to/output.png" 10.0 5.0 "png"
```

### ClipImage

裁剪图像的指定区域。

- **功能**: 从源图像中裁剪指定矩形区域，生成裁剪后的图像文件
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 头像裁剪、截图区域选取

- **输入参数**:
  - `srcFile`（string, 类型 `s`）：源图像路径
  - `dstFile`（string, 类型 `s`）：目标图像路径
  - `x`（int32, 类型 `i`）：裁剪区域左上角 x 坐标
  - `y`（int32, 类型 `i`）：裁剪区域左上角 y 坐标
  - `w`（int32, 类型 `i`）：裁剪区域宽度
  - `h`（int32, 类型 `i`）：裁剪区域高度
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.ClipImage \
  "/path/to/input.png" "/path/to/output.png" 0 0 100 100 "png"
```

### CompositeImage

将两张图像合成为一张。

- **功能**: 将叠加图像合成到源图像的指定位置，生成合成后的图像文件
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 图片水印叠加、图标合成

- **输入参数**:
  - `srcFile`（string, 类型 `s`）：源图像路径
  - `compFile`（string, 类型 `s`）：叠加图像路径
  - `dstFile`（string, 类型 `s`）：目标图像路径
  - `x`（int32, 类型 `i`）：叠加位置 x 坐标
  - `y`（int32, 类型 `i`）：叠加位置 y 坐标
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.CompositeImage \
  "/path/to/base.png" "/path/to/overlay.png" "/path/to/output.png" 10 10 "png"
```

### CompositeImageUri

将两个 data URI 格式的图像合成为一个 data URI。

- **功能**: 将两个 data URI 格式的图像合成为一个新的 data URI，无需中间文件
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 前端组件中直接处理 data URI 格式图像的合成

- **输入参数**:
  - `srcDataUri`（string, 类型 `s`）：源图像的 data URI
  - `compDataUri`（string, 类型 `s`）：叠加图像的 data URI
  - `x`（int32, 类型 `i`）：叠加位置 x 坐标
  - `y`（int32, 类型 `i`）：叠加位置 y 坐标
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: `resultDataUri`（string, 类型 `s`）：合成后的 data URI

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.CompositeImageUri \
  "data:image/png;base64,..." "data:image/png;base64,..." 10 10 "png"
```

### ConvertDataUriToImage

将 data URI 转换为图像文件。

- **功能**: 将 data URI 格式的图像数据解码并保存为图像文件
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 将前端传递的 data URI 图像保存为本地文件

- **输入参数**:
  - `dataUri`（string, 类型 `s`）：图像的 data URI
  - `dstFile`（string, 类型 `s`）：目标图像路径
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.ConvertDataUriToImage \
  "data:image/png;base64,..." "/path/to/output.png" "png"
```

### ConvertImage

将图像从一种格式转换为另一种格式。

- **功能**: 将图像文件从原始格式转换为目标格式（如 BMP 转 PNG）
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 图像格式统一转换、适配不同组件的格式需求

- **输入参数**:
  - `srcFile`（string, 类型 `s`）：源图像路径
  - `dstFile`（string, 类型 `s`）：目标图像路径
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.ConvertImage \
  "/path/to/input.bmp" "/path/to/output.png" "png"
```

### ConvertImageToDataUri

将图像文件转换为 data URI。

- **功能**: 将图像文件编码为 data URI 格式字符串
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 将本地图像传递给前端组件使用

- **输入参数**:
  - `imgfile`（string, 类型 `s`）：图像文件路径
- **返回值**: `dataUri`（string, 类型 `s`）：图像的 data URI

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.ConvertImageToDataUri \
  "/path/to/input.png"
```

### FillImage

将图像填充到指定尺寸。

- **功能**: 将源图像扩展填充到指定的宽度和高度，生成填充后的图像文件
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 将图片适配到固定尺寸的容器中

- **输入参数**:
  - `srcFile`（string, 类型 `s`）：源图像路径
  - `dstFile`（string, 类型 `s`）：目标图像路径
  - `width`（int32, 类型 `i`）：目标宽度
  - `height`（int32, 类型 `i`）：目标高度
  - `style`（string, 类型 `s`）：填充样式（如 `tile`、`center`）
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.FillImage \
  "/path/to/input.png" "/path/to/output.png" 800 600 "center" "png"
```

### FlipImageHorizontal

将图像水平翻转。

- **功能**: 沿垂直轴翻转图像，生成翻转后的图像文件
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 镜像翻转图片、摄像头预览镜像处理

- **输入参数**:
  - `srcFile`（string, 类型 `s`）：源图像路径
  - `dstFile`（string, 类型 `s`）：目标图像路径
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.FlipImageHorizontal \
  "/path/to/input.png" "/path/to/output.png" "png"
```

### FlipImageVertical

将图像垂直翻转。

- **功能**: 沿水平轴翻转图像，生成翻转后的图像文件
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 图片倒置处理

- **输入参数**:
  - `srcFile`（string, 类型 `s`）：源图像路径
  - `dstFile`（string, 类型 `s`）：目标图像路径
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.FlipImageVertical \
  "/path/to/input.png" "/path/to/output.png" "png"
```

### GetDominantColorOfImage

获取图像的主色调（HSV 格式）。

- **功能**: 分析图像像素，提取主色调并以 HSV 格式返回
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 根据壁纸主色调自动调整界面配色

- **输入参数**:
  - `imgFile`（string, 类型 `s`）：图像文件路径
- **返回值**:
  - `h`（double, 类型 `d`）：色相（0~360）
  - `s`（double, 类型 `d`）：饱和度（0~1）
  - `v`（double, 类型 `d`）：明度（0~1）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.GetDominantColorOfImage \
  "/path/to/input.png"
```

### GetImageSize

获取图像的宽度和高度。

- **功能**: 读取图像文件的尺寸信息
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 获取图片尺寸以进行布局适配

- **输入参数**:
  - `imgFile`（string, 类型 `s`）：图像文件路径
- **返回值**:
  - `width`（int32, 类型 `i`）：图像宽度
  - `height`（int32, 类型 `i`）：图像高度

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.GetImageSize \
  "/path/to/input.png"
```

### Hsv2Rgb

将 HSV 颜色转换为 RGB 颜色。

- **功能**: 将 HSV 色彩空间的值转换为 RGB 色彩空间的值
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 界面配色计算、主题颜色转换

- **输入参数**:
  - `h`（double, 类型 `d`）：色相（0~360）
  - `s`（double, 类型 `d`）：饱和度（0~1）
  - `v`（double, 类型 `d`）：明度（0~1）
- **返回值**:
  - `r`（uint8, 类型 `y`）：红色分量（0~255）
  - `g`（uint8, 类型 `y`）：绿色分量（0~255）
  - `b`（uint8, 类型 `y`）：蓝色分量（0~255）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Hsv2Rgb \
  120.0 1.0 1.0
```

### ResizeImage

调整图像尺寸到指定的宽度和高度。

- **功能**: 将图像缩放到指定的宽度和高度，生成调整后的图像文件
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 壁纸缩放、头像尺寸调整

- **输入参数**:
  - `srcFile`（string, 类型 `s`）：源图像路径
  - `dstFile`（string, 类型 `s`）：目标图像路径
  - `newWidth`（int32, 类型 `i`）：目标宽度
  - `newHeight`（int32, 类型 `i`）：目标高度
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.ResizeImage \
  "/path/to/input.png" "/path/to/output.png" 800 600 "png"
```

### Rgb2Hsv

将 RGB 颜色转换为 HSV 颜色。

- **功能**: 将 RGB 色彩空间的值转换为 HSV 色彩空间的值
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 颜色分析、基于色相的颜色分类

- **输入参数**:
  - `r`（uint8, 类型 `y`）：红色分量（0~255）
  - `g`（uint8, 类型 `y`）：绿色分量（0~255）
  - `b`（uint8, 类型 `y`）：蓝色分量（0~255）
- **返回值**:
  - `h`（double, 类型 `d`）：色相（0~360）
  - `s`（double, 类型 `d`）：饱和度（0~1）
  - `v`（double, 类型 `d`）：明度（0~1）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.Rgb2Hsv \
  0x00 0xff 0x00
```

### RotateImageLeft

将图像向左旋转 90 度。

- **功能**: 将图像逆时针旋转 90 度，生成旋转后的图像文件
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 图片方向调整、截图旋转

- **输入参数**:
  - `srcFile`（string, 类型 `s`）：源图像路径
  - `dstFile`（string, 类型 `s`）：目标图像路径
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.RotateImageLeft \
  "/path/to/input.png" "/path/to/output.png" "png"
```

### RotateImageRight

将图像向右旋转 90 度。

- **功能**: 将图像顺时针旋转 90 度，生成旋转后的图像文件
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 图片方向调整、截图旋转

- **输入参数**:
  - `srcFile`（string, 类型 `s`）：源图像路径
  - `dstFile`（string, 类型 `s`）：目标图像路径
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.RotateImageRight \
  "/path/to/input.png" "/path/to/output.png" "png"
```

### ThumbnailImage

按最大宽度和高度限制生成缩略图（按比例缩放）。

- **功能**: 在不超过最大宽度和高度的前提下，按原始比例缩放图像生成缩略图
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 文件管理器缩略图生成、图片预览

- **输入参数**:
  - `srcFile`（string, 类型 `s`）：源图像路径
  - `dstFile`（string, 类型 `s`）：目标图像路径
  - `maxWidth`（uint32, 类型 `u`）：最大宽度
  - `maxHeight`（uint32, 类型 `u`）：最大高度
  - `format`（string, 类型 `s`）：输出格式（`png` 或 `jpeg`）
- **返回值**: 无（出错时返回 dbus.Error）

```bash
gdbus call --session \
  --dest org.deepin.dde.Graphic1 \
  --object-path /org/deepin/dde/Graphic1 \
  --method org.deepin.dde.Graphic1.ThumbnailImage \
  "/path/to/input.png" "/path/to/output.png" 200 200 "png"
```
