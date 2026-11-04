# dtk6-svgc 命令参考

SVG 转 PNG 转换工具，支持指定渲染器、缩放因子和输出尺寸。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DWidget/bin/dtk6-svgc` |
| DDE 角色 | 开发辅助工具，用于将 SVG 文件转换为 PNG 图片 |

## 用途

SVG 转 PNG 转换工具。读取 SVG 文件，使用指定的渲染器（`DSvgRenderer` 或 `QSvgRenderer`）将其渲染为 PNG 图片。支持通过缩放因子和输出尺寸控制最终图片的分辨率。适用于 DTK 应用中 SVG 图标资源的批量转换和预览生成开发。

## 用法

`dtk6-svgc [options] <input> <output>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-r, --render <renderer>` | 指定 SVG 渲染器：`DSvgRenderer` 或 `QSvgRenderer`（默认 `QSvgRenderer`） | 是 |
| `-f, --factor <factor>` | 缩放因子，必须大于 0（默认 1.0） | 是 |
| `-s, --size <WxH>` | 输出尺寸，格式为 `宽x高`，例如 `100x200`、`100x`、`x200` | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `input` | 输入的 SVG 文件路径 |
| `output` | 输出的 PNG 文件路径 |

## 使用示例

```bash
# 使用默认渲染器转换 SVG 为 PNG
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc input.svg output.png

# 使用 DSvgRenderer 渲染器转换
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc -r DSvgRenderer input.svg output.png

# 指定缩放因子为 2.0
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc -f 2.0 input.svg output.png

# 指定输出尺寸为 100x200
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc -s 100x200 input.svg output.png

# 仅指定宽度（高度按比例缩放）
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc -s 100x input.svg output.png

# 组合使用渲染器、缩放因子和输出尺寸
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc -r DSvgRenderer -f 2.0 -s 256x256 input.svg output.png

# 查看帮助信息
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc --help
```
