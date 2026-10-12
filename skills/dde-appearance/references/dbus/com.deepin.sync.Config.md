# com.deepin.sync.Config 接口参考

该接口为 dde-appearance 内部同步辅助接口，用于 UOS ID 数据同步场景下的外观配置序列化读写。dde-appearance 在 Session 总线上以同一接口名 `com.deepin.sync.Config` 注册两个对象路径，分别负责主题字体同步和壁纸背景同步。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Appearance1` |
| Object path | `/org/deepin/dde/Appearance1/sync`、`/org/deepin/dde/Appearance1/Background` |
| Interface | `com.deepin.sync.Config` |
| Bus | Session |

## 注册路径说明

### `/org/deepin/dde/Appearance1/sync`

主题字体同步配置。负责字体大小、GTK 主题、图标主题、光标主题、标准字体、等宽字体六项外观属性的序列化与反序列化。

### `/org/deepin/dde/Appearance1/Background`

壁纸背景同步配置。负责壁纸 URI 列表、壁纸幻灯片轮播配置、登录锁屏背景图片的序列化与反序列化。

## 方法（Methods）

### Get

获取当前同步配置的序列化数据。

- **输入参数**: 无
- **返回值**: `data`（QByteArray, 类型 `ay`）— JSON 格式的配置数据
- **触发条件**: UOS ID 同步服务请求读取本机外观配置时调用
- **使用场景**: 当 UOS ID 同步服务需要采集当前设备的外观配置以同步到云端或其他设备时使用。

**`/org/deepin/dde/Appearance1/sync` 返回的 JSON 字段**:

```json
{
  "version": "1.0",
  "font_size": 11.0,
  "gtk": "deepin",
  "icon": "bloom",
  "cursor": "deepin",
  "font_standard": "Noto Sans CJK SC",
  "font_monospace": "Noto Sans Mono CJK SC"
}
```

**`/org/deepin/dde/Appearance1/Background` 返回的 JSON 字段**:

```json
{
  "version": "2.0",
  "slide_show_config": {
    "eDP-1&&1": "180"
  },
  "wallpaper_uris": {
    "eDP-1&&1": "file:///usr/share/wallpapers/deepin/desktop.jpg"
  },
  "greeter_background": "file:///usr/share/wallpapers/deepin/desktop.jpg"
}
```

### Set

从序列化数据恢复外观配置。

- **输入参数**:
  - `data`（QByteArray, 类型 `ay`）— JSON 格式的配置数据
- **返回值**: 无
- **触发条件**: UOS ID 同步服务将云端或其他设备的外观配置下发到本机时调用
- **使用场景**: 当 UOS ID 同步服务将其他设备的外观配置同步到当前设备时使用，接口解析 JSON 数据并逐项应用差异化的外观设置。

**`/org/deepin/dde/Appearance1/sync` 接受的 JSON 字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `font_size` | double | 字体大小 |
| `gtk` | string | GTK 主题名称 |
| `icon` | string | 图标主题名称 |
| `cursor` | string | 光标主题名称 |
| `font_standard` | string | 标准字体名称 |
| `font_monospace` | string | 等宽字体名称 |

**`/org/deepin/dde/Appearance1/Background` 接受的 JSON 字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `version` | string | 配置版本号，`"1.0"` 使用旧版字段格式，`"2.0"` 使用新版字段格式 |
| `greeter_background` | string | 登录锁屏背景图片 URI |
| `slide_show` | string | （仅 version `"1.0"`）壁纸幻灯片轮播间隔 |
| `background_uris` | array | （仅 version `"1.0"`）各工作区壁纸 URI 数组 |
| `slide_show_config` | object | （version `"2.0"`）壁纸幻灯片轮播配置，键格式为 `显示器名&&工作区序号` |
| `wallpaper_uris` | object | （version `"2.0"`）壁纸 URI 配置，键格式为 `显示器名&&工作区序号` |

## gdbus 示例

> 注意：`com.deepin.sync.Config` 接口由 `org.deepin.dde.Appearance1` 服务在内部注册，非独立服务。以下示例需在 dde-appearance 服务正常运行的环境中执行。

```bash
# 获取主题字体同步配置
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1/sync \
  --method com.deepin.sync.Config.Get

# 设置主题字体同步配置
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1/sync \
  --method com.deepin.sync.Config.Set '[{"version": "1.0", "font_size": 12.0, "gtk": "deepin", "icon": "bloom", "cursor": "deepin", "font_standard": "Noto Sans CJK SC", "font_monospace": "Noto Sans Mono CJK SC"}]'

# 获取壁纸背景同步配置
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1/Background \
  --method com.deepin.sync.Config.Get

# 设置壁纸背景同步配置
gdbus call --session \
  --dest org.deepin.dde.Appearance1 \
  --object-path /org/deepin/dde/Appearance1/Background \
  --method com.deepin.sync.Config.Set '[{"version": "2.0", "greeter_background": "file:///usr/share/wallpapers/deepin/desktop.jpg", "slide_show_config": {}, "wallpaper_uris": {}}]'
```
