# dci-image-converter 命令参考

DCI 图片格式转换工具，用于在 DCI（Deepin Custom Image）格式与 alpha8 格式之间进行相互转换。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | 不安装（仅源码构建产物） |
| DDE 角色 | 开发调试工具，用于 DCI 图片资源构建和转换 |

## 用途

DCI 图片格式转换工具，用于在 DCI（Deepin Custom Image）格式与 alpha8 格式之间进行相互转换。DCI 是 DTK 框架自研的图片格式，支持多分辨率、状态切换和动画效果，广泛用于 DDE 图标和 UI 图片资源。alpha8 是一种优化的中间格式，主要用于减小资源体积。该工具是 DTK 开发工具链的一部分，供开发者和主题设计者在资源构建流程中使用。

## 用法

`dci-image-converter [options] <sourcesPath>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `--version` | 显示版本信息 | 否 |
| `--toAlpha8 <targetPath>` | 将图片格式转换为 alpha8 | 是 |
| `--fromAlpha8 <targetPath>` | 从 alpha8 格式转换图片格式 | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `sourcesPath` | 待转换的文件路径（可多个） |

## 使用示例

```bash
# 将 DCI 图片转换为 alpha8 格式
dci-image-converter --toAlpha8 /tmp/output/ /usr/share/dsg/icons/bloom/icons/app.dci

# 将 alpha8 格式图片转换回 DCI 格式
dci-image-converter --fromAlpha8 /tmp/output/ /tmp/alpha8-images/img.a8

# 批量转换多个 DCI 文件为 alpha8
dci-image-converter --toAlpha8 /tmp/output/ icon1.dci icon2.dci icon3.dci
```
