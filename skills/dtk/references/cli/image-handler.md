# image-handler 命令参考

DTK 图片处理工具，支持图片旋转、应用滤镜效果、查看图片信息三项操作。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | 不安装（仅源码构建产物） |
| DDE 角色 | 开发调试工具，也可用于简单的图片处理 |

## 用途

DTK 图片处理工具，支持图片旋转、应用滤镜效果、查看图片信息三项操作。内置多种滤镜效果（old 复古、warm 暖色、cool 冷色、gray 灰度、anticolor 反色、metal 金属），可以按指定角度旋转图片并保存到文件。还支持列出所有支持的图片格式和显示额外图片元信息。该工具适用于简单的图片处理需求，也是 DTK 图片处理功能的命令行接口。

## 用法

`image-handler [options] <file>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-r, --rotate <degrees>` | 旋转图片（角度） | 是 |
| `-o, --output <file>` | 保存图片到文件 | 是 |
| `-f <filter>` | 应用滤镜：`old`/`warm`/`cool`/`gray`/`anticolor`/`metal` | 是 |
| `-e` | 显示额外图片信息 | 否 |
| `-l, --list` | 列出所有支持的图片格式 | 否 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `file` | 待打开的文件（可多个） |

## 使用示例

```bash
# 旋转图片 90 度并保存到新文件
image-handler -r 90 -o /tmp/rotated.jpg /home/user/photo.jpg

# 应用灰度滤镜并保存
image-handler -f gray -o /tmp/gray.jpg /home/user/photo.jpg

# 应用暖色滤镜并保存
image-handler -f warm -o /tmp/warm.jpg /home/user/photo.jpg

# 显示图片的额外信息（尺寸、格式、色彩空间）
image-handler -e /home/user/photo.jpg

# 列出所有支持的图片格式
image-handler -l

# 旋转 180 度并应用金属滤镜
image-handler -r 180 -f metal -o /tmp/processed.jpg /home/user/photo.jpg

# 同时处理多个文件
image-handler -f cool /home/user/photo1.jpg /home/user/photo2.jpg
```
