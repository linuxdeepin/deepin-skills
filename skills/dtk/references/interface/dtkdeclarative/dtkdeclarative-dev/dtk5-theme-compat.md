# DTK5 主题兼容

提供平台主题代理和系统调色板 QML 项，仅在 DTK5 中提供，DTK6 已移除。

## DPlatformThemeProxy

### 定位

平台主题的 QML 代理接口（仅 DTK5）。

### 功能能力总结

将 DTK 平台主题的平台主题属性（主题色、字号、图标主题）暴露为 QML 可访问的属性和信号。DTK6 已移除此类型，相关功能由 QML 层直接提供。

### 使用场景

DTK5 QML 应用中需要读取或监听平台主题属性变化时。


---

## DQuickSystemPalette

### 定位

QML 系统调色板项（仅 DTK5，已废弃）。

### 功能能力总结

将系统调色板暴露为 QML 可访问的属性，支持 Active、Inactive、Disabled 三种颜色组。已废弃，应使用 `DQMLGlobalObject::palette` 替代。DTK6 已移除此类型。

### 使用场景

已废弃，DTK5 中如需在 QML 中访问系统调色板时可使用，新代码应迁移至 `DQMLGlobalObject::palette`。
