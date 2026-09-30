# image-blur 命令参考

图片模糊处理工具，使用高斯模糊算法对图片进行模糊处理。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-api` |
| 安装路径 | `/usr/lib/deepin-api/image-blur` |
| DDE 角色 | 系统调用的图片处理辅助工具 |

## 用途

图片模糊处理工具，使用高斯模糊算法对图片进行模糊处理。它接受输入图片文件路径和输出文件路径，通过 `-sigma` 参数控制模糊强度（默认 20.0，值越大模糊程度越高）。该工具主要用于 DDE 界面中需要模糊背景效果的场景，例如锁屏壁纸的模糊处理和控制中心的毛玻璃效果背景。通常由系统主题组件或壁纸管理模块调用。使用 Go flag 风格参数。

## 用法

`/usr/lib/deepin-api/image-blur [options] <input> <output>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-sigma <float>` | 模糊强度（默认 20.0） | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| input | 输入图片文件 |
| output | 输出图片文件 |

## 使用示例

```bash
# 使用默认模糊强度（20.0）处理图片
/usr/lib/deepin-api/image-blur /home/user/wallpaper.jpg /tmp/wallpaper-blurred.jpg

# 指定模糊强度为 10.0（较轻微的模糊）
/usr/lib/deepin-api/image-blur -sigma 10.0 /home/user/wallpaper.jpg /tmp/wallpaper-blurred.jpg

# 指定模糊强度为 50.0（较强的模糊效果）
/usr/lib/deepin-api/image-blur -sigma 50.0 /home/user/wallpaper.jpg /tmp/wallpaper-blurred.jpg
```
