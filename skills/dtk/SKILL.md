---
name: dtk
description: DTK 开发套件提供的跨进程文件拖拽 D-Bus 接口和 DTK 应用偏好与区域格式 DConfig 配置能力
Categories:
  - Develop
---

# dtk

DTK（Deepin Tool Kit）是 Deepin 桌面环境的开发套件。本 skill 描述 DTK 对外提供的 D-Bus 接口和 DConfig 公共配置能力。

## D-Bus 接口

### 文件拖拽服务

提供跨进程文件拖拽交互能力。拖拽源进程在 Session 总线上注册此接口对象，文件接收方通过 D-Bus 与拖拽源通信，实现拖拽状态查询、进度同步和数据回传。接口使用动态 baseService（拖拽源进程的唯一连接名），接收方从拖拽 MIME 数据中获取 service 名称和会话 UUID 后调用。

- **Bus**: Session
- **Service**: `<dynamic baseService>`（如 `:1.23`）
- **Object path**: `/Ddnd`
- **Interface**: `com.deepin.dtk.FileDrag`
- **方法**: `setData`（设置会话数据）、`state`（查询状态）、`progress`（查询进度）
- **信号**: `serverDestroyed`（会话销毁）、`stateChanged`（状态变化）、`progressChanged`（进度变化）、`targetDataChanged`（目标数据变更）

详见 [com.deepin.dtk.FileDrag](references/dbus/com.deepin.dtk.FileDrag.md)

## DConfig 配置

DTK 通过 DConfig 暴露两组公共配置资源（appId 为空，所有 DTK 应用共享）。

### DTK 应用偏好配置

控制以下 DTK 应用的外观与行为：主题、动画、滚动条、标题栏、新特性展示、菜单搜索、日志规则，共 11 项配置。

配置项：`autoDisplayFeature`、`defaultColorMode`、`enableDtkAnimations`、`featureUpdated`、`keyboardsearchDisabled`、`rules`、`scrollBarPolicy`、`sizeMode`、`themeType`、`titlebarHeight`、`underlineShortcut`

详见 [org.deepin.dtk.preference](references/config/org.deepin.dtk.preference.md)

### 区域格式配置

控制以下系统的区域格式：语言、日期、时间、数字、货币、纸张，共 11 项配置。

配置项：`country`、`currencyFormat`、`firstDayOfWeek`、`languageRegion`、`localeName`、`longDateFormat`、`longTimeFormat`、`numberFormat`、`paperFormat`、`shortDateFormat`、`shortTimeFormat`

详见 [org.deepin.region-format](references/config/org.deepin.region-format.md)
