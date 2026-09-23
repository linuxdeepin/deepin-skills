# org.freedesktop.impl.portal.Screenshot 接口参考

该接口提供屏幕截图能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.freedesktop.impl.portal.desktop.dde` |
| Object path | `/org/freedesktop/portal/desktop` |
| Interface | `org.freedesktop.impl.portal.Screenshot` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 截图方法

#### Screenshot

进行屏幕截图。

- **输入参数**: `parent_handle`（object, 类型 `o`）：父窗口句柄；`options`（字典, 类型 `a{sv}`）：截图选项
- **返回值**: `o`（object path）：请求路径

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Screenshot.Screenshot "" {}
```

#### ScreenshotColor

进行屏幕取色截图。

- **输入参数**: `parent_handle`（object, 类型 `o`）：父窗口句柄；`options`（字典, 类型 `a{sv}`）：截图选项
- **返回值**: `o`（object path）：请求路径

```bash
gdbus call --session \
  --dest org.freedesktop.impl.portal.desktop.dde \
  --object-path /org/freedesktop/portal/desktop \
  --method org.freedesktop.impl.portal.Screenshot.ScreenshotColor "" {}
```

