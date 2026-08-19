# dde-control-center-focusmode

一个用于演示 **DDE 控制中心插件完整开发流程** 的独立示例项目 —— **专注模式（Focus Mode）** 插件。

本项目是一个**独立、可独立构建与打包**的控制中心插件工程，覆盖从项目结构、C++ 数据对象、
QML 界面、DConfig 持久化、系统通知、翻译到 Debian 打包的完整链路。

> 说明：本插件**只负责管理专注模式的状态**（开启/关闭、持久化、通知用户）。
> 真正的专注业务（拦截通知、屏蔽打扰等）由**其它服务**监听本插件写入的
> DConfig 状态自行处理，不在此插件内实现。

---

## 功能特性

- ✅ 在控制中心中打开/关闭专注模式（`DccGroupView` + `Editor` 开关）
- ✅ 状态持久化：通过 `DConfig` 写入系统配置，重启后保持
- ✅ 系统通知：状态变化时通过 `org.freedesktop.Notifications` 发送通知
- ✅ 跨服务共享：其它服务可监听 DConfig `valueChanged` 读取/响应状态
- ✅ 多语言：通过 `.ts` 翻译文件支持常见语言（en_US / zh_CN / zh_TW 等）
- ✅ Debian 打包：`debian/` 目录提供完整打包配置

---

## 项目结构

```
dde-control-center-focusmode/
├── CMakeLists.txt                # 构建脚本（dcc_install_plugin / 翻译 / DConfig 安装）
├── README.md                     # 本文档
├── src/                          # C++ 源码
│   ├── focusmode.h / .cpp        # 数据对象（DCC_FACTORY_CLASS 注册，QML 中作为 dccData）
│   └── focusmodeworker.h / .cpp  # 后台工作类（DConfig 持久化 + 系统通知）
├── qml/                          # QML 界面
│   ├── Focusmode.qml             # 模块元数据（根 DccObject，不能使用 dccData）
│   ├── FocusmodeMain.qml         # 主页面（设置直接挂模块下，第二级，可使用 dccData）
│   └── metadata.json             # 插件元数据 {"Version": "1.0"}
├── configs/
│   └── org.deepin.dde.control-center.focusmode.json  # DConfig 元数据
├── data/icons/
│   ├── deepin-dde.dci           # 模块图标（内置 DCI 图标）
│   └── icons.qrc               # 内置图标资源（/dsg/built-in-icons/）
├── translations/                 # 翻译文件
│   ├── focusmode.ts              # 源字符串模板
│   ├── focusmode_en_US.ts
│   ├── focusmode_zh_CN.ts
│   └── focusmode_zh_TW.ts
└── debian/                       # Debian 打包配置
    ├── control
    ├── rules
    ├── compat
    ├── changelog
    ├── copyright
    └── source/format
```

---

## 图标（内置 DCI 图标）

模块图标 `deepin-dde.dci` 采用 **内置（built-in）** 方式，编译进插件自身资源，
**不安装到系统**，避免与其它应用冲突：

- 源码位于 `data/icons/deepin-dde.dci`，由 `data/icons/icons.qrc` 编译进插件
  资源命名空间 `/dsg/built-in-icons/`
- 界面通过基础名引用 `icon: "deepin-dde"`，`DDciIcon::fromTheme("deepin-dde")`
  走 DTK 的内置兜底路径 `:/dsg/built-in-icons/` 解析，无需任何系统安装
- 插件加载时在模块构造函数中 `Q_INIT_RESOURCE(icons)` 显式注册资源
- 系统通知的 `app_icon` 同样使用 `deepin-dde`

图标随插件一起分发，自包含、不污染系统图标主题，也不会与其它包同名冲突。

---

## 架构说明

本插件采用控制中心推荐的 **Model-Worker 分层**（类似蓝牙插件的 Interaction-Model-Worker 简化版）：

```
FocusModeModule (数据对象, dccData)
   └── FocusModeWorker (后台工作类)
         ├── DConfig          → 状态持久化 + 跨服务共享
         └── DDBusSender      → 系统通知
```

- **FocusModeModule**：插件入口，通过 `DCC_FACTORY_CLASS` 注册。暴露 `enabled`
  属性与 `setEnabled()` 供 QML 调用。所有子对象（`FocusModeWorker`）都挂到
  `this` 的 QObject 树中，保证线程池加载后能随主线程正确迁移。
- **FocusModeWorker**：真正处理状态。加载 DConfig、写回状态、监听外部修改、
  发送系统通知。

### 状态管理（DConfig）

- `appId`：`org.deepin.dde.control-center`（**必须**是宿主应用的应用标识，插件不能单独构造 appId）
- `configId`：`org.deepin.dde.control-center.focusmode`
- 配置项：`enabled`（bool，`visibility: public`，`flags: ["user-public"]`）

插件把开关状态写入 `enabled`，同时监听 `valueChanged` 以便其它服务修改时
同步回 UI。

### 其它服务如何消费状态

本插件只写状态。需要处理专注业务的其它服务（独立进程/应用）可以这样订阅：

```cpp
#include <DConfig>

// 消费方与插件使用相同的 appId 和 configId
auto *config = DConfig::create("org.deepin.dde.control-center",
                               "org.deepin.dde.control-center.focusmode", "", this);

// 1. 读取当前状态
const bool enabled = config->isValid() ? config->value("enabled", false).toBool() : false;

// 2. 监听状态变化并执行专注业务
connect(config, &DConfig::valueChanged, this, [](const QString &key) {
    if (key == "enabled") {
        // 读取新状态并应用专注行为（拦截通知、屏蔽打扰等）
    }
});
```

这样实现了「本插件只管理状态，业务由其它服务处理」的职责分离。

---

## 构建

### 依赖

- `dde-control-center-dev`：提供插件头文件、`find_package(DdeControlCenter)` 与 CMake 宏
- `qt6-base-dev`、`qt6-declarative-dev`、`qt6-tools-dev`
- `libdtk6core-dev`（提供 DConfig / DDBusSender）

### 编译

```bash
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr
make -j$(nproc)
```

### 安装到本地（供调试）

```bash
sudo make install
```

---

## 调试

控制中心支持 `--spec` 指定插件搜索路径，仅修改插件时可用：

```bash
# 使用构建目录中的插件
./dde-control-center --spec ./build/lib/plugins_v1.1/
```

> 若同时修改了控制中心框架库或 QML 引擎组件，还需要设置
> `LD_LIBRARY_PATH`、`QT_PLUGIN_PATH`、`QML2_IMPORT_PATH` 指向构建目录，
> 否则运行时仍会加载系统安装版本。详见 skill 的 debugging 文档。

### 常见问题

| 现象 | 排查 |
|------|------|
| 插件不显示 | `Focusmode.qml` 中 `visible`、`hideModule`/`disableModule` 配置、`DccDBusInterface` 条件 |
| `dccData` 为 undefined | 是否在 `Focusmode.qml`（根元数据）中访问了 dccData；`DCC_FACTORY_CLASS` 是否正确；是否 include 了 `.moc` |
| QML 修改无效 | 文件名是否首字母大写、是否为 `main.qml`、是否清除了 QML 缓存 |
| 加载崩溃 | 子对象是否都纳入了 QObject 树（线程安全） |

---

## 翻译

- QML 中使用 `qsTr()`，C++ 中使用 `tr()`（类继承 `QObject` 且使用 `Q_OBJECT`）。
- `dcc_handle_plugin_translation` 会自动处理并安装翻译。
- 新增语言时在 `translations/` 下添加 `focusmode_<locale>.ts` 即可；
  生产环境通常通过 tx 工具推送到翻译平台，不手动编辑。

---

## Debian 打包

```bash
# 在项目根目录执行
dpkg-buildpackage -us -uc -b
```

生成的 `.deb` 包含：

- 插件动态库与 QML 资源 → `/usr/lib/{multiarch}/dde-control-center/plugins_v1.1/focusmode/`
- 翻译 → `/usr/share/dde-control-center/translations/v1.1/`
- DConfig 元数据 → `/usr/share/dsg/configs/org.deepin.dde.control-center/`

运行时依赖 `dde-control-center`，构建依赖 `dde-control-center-dev`。

---

## 许可证

本项目采用 GPL-3.0-or-later 许可，详见 `debian/copyright`。
