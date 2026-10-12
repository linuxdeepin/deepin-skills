# dtk6-svgc 命令参考

SVG 转 PNG 转换工具，将 SVG 矢量图渲染为 PNG 位图。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DWidget/bin/dtk6-svgc` |
| DDE 角色 | 开发工具，用于 SVG 图片转 PNG |

## 用途

SVG 转 PNG 转换工具，将 SVG 矢量图渲染为 PNG 位图。支持通过 `DSvgRenderer`（DTK 增强渲染器）或 `QSvgRenderer`（Qt 原生渲染器）进行渲染，支持指定输出尺寸（宽x高、仅宽、仅高）和缩放因子。该工具适用于 SVG 图标资源的位图化处理。

## 用法

`dtk6-svgc [options] <input> <output>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-r, --render <render>` | 渲染器：`DSvgRenderer`（DTK 增强）或 `QSvgRenderer`（Qt 原生，默认） | 是 |
| `-f, --factor <factor>` | 缩放因子，必须 > 0，默认 1.0 | 是 |
| `-s, --size <size>` | 输出尺寸，格式为 `宽x高`（如 `100x200`）、`100x`（仅指定宽）、`x200`（仅指定高） | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `input` | 输入 SVG 文件路径 |
| `output` | 输出 PNG 文件路径 |

## 使用示例

```bash
# 将 SVG 转为 PNG（默认尺寸和渲染器）
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc icon.svg icon.png

# 指定输出尺寸为 100x200
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc -s 100x200 icon.svg icon.png

# 仅指定宽度，高度按比例缩放
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc -s 100x icon.svg icon.png

# 仅指定高度，宽度按比例缩放
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc -s x200 icon.svg icon.png

# 使用 DTK 增强渲染器
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc -r DSvgRenderer icon.svg icon.png

# 使用 2 倍缩放因子
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc -f 2.0 icon.svg icon.png

# 查看帮助信息
/usr/libexec/dtk6/DWidget/bin/dtk6-svgc --help
```
