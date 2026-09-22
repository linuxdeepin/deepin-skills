# org.deepin.dde.Osd1 接口参考

该接口提供 OSD（On-Screen Display）提示的显示能力，支持通过 OSD 类型标识触发对应的屏幕提示显示。

> **待核验**: `ShowOSD` 接受的 `text` 参数为 OSD 类型标识字符串。源码中可见 `SwitchWM3D` 作为特殊值（显示时长不同），其他支持的 OSD 标识需运行时核验。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Osd1` |
| Object path | `/` |
| Interface | `org.deepin.dde.Osd1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

## 方法、属性与信号

### OSD 显示

#### ShowOSD

显示 OSD 提示。

- **输入参数**:
  - `text`（string, 类型 `s`）：OSD 类型标识（如 `SwitchWM3D`）
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Osd1 \
  --object-path / \
  --method org.deepin.dde.Osd1.ShowOSD "SwitchWM3D"
```

---
