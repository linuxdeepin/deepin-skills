# org.deepin.screensaver

屏保主配置资源，管理当前使用的屏幕保护程序。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `currentScreenSaver` | 当前屏保 | 配置当前使用的屏幕保护程序 | string | readwrite |

## 读写示例

```bash
# 查询当前屏保
dde-dconfig get -a org.deepin.screensaver -r org.deepin.screensaver -k currentScreenSaver
# 设置当前屏保
dde-dconfig set -a org.deepin.screensaver -r org.deepin.screensaver -k currentScreenSaver -v "<value>"
```
