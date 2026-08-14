# DTK 应用开发项目配置

> 适用场景：创建新的应用项目，需要依赖 DTK 库。覆盖 CMake 配置、头文件引用、日志集成和最小示例。

---

## 0. 版本前置检查

检查目标工程实际使用的 Qt/DTK 和构建系统。以下 DTK6 模板面向 v25；v20
不得使用 `Qt6`、`Dtk6*` 包或 v25 专有 API。

v20 应用使用 Qt 5.11/DTK5：

```cmake
find_package(Qt5 REQUIRED COMPONENTS Core Widgets)
find_package(DtkCore REQUIRED)
find_package(DtkGui REQUIRED)
find_package(DtkWidget REQUIRED)

target_link_libraries(myapp PRIVATE
    Qt5::Core Qt5::Widgets
    Dtk::Core Dtk::Gui Dtk::Widget
)
```

如果现有 v20 工程使用 qmake，保留其 `.pro`/`.pri` 结构和已有模块名。DConfig
与 DCI 使用 v20 档案的接口。v20 QML 不添加任何 DTK Declarative 依赖，直接使用：

```qml
import QtQuick 2.11
import QtQuick.Controls 2.4
```

## 1. 项目 CMake 配置

### 1.1 标准 CMakeLists.txt 模板

#### DTK6（v25 推荐）

```cmake
cmake_minimum_required(VERSION 3.13)
project(myapp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets)
find_package(Dtk6Core REQUIRED)
find_package(Dtk6Gui REQUIRED)
find_package(Dtk6Widget REQUIRED)

add_executable(myapp
    main.cpp
    mainwindow.cpp
)

target_link_libraries(myapp PRIVATE
    Qt6::Core
    Qt6::Widgets
    Dtk6::Core
    Dtk6::Gui
    Dtk6::Widget
)
```

### 1.2 v25 兼容 DTK5 和 DTK6

```cmake
cmake_minimum_required(VERSION 3.13)
project(myapp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# 自动检测 Qt 版本
find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core Widgets)

# 根据 Qt 版本决定 DTK 后缀
if(QT_VERSION_MAJOR EQUAL 6)
    set(DTK_SUFFIX 6)
else()
    set(DTK_SUFFIX "")
endif()

find_package(Dtk${DTK_SUFFIX}Core REQUIRED)
find_package(Dtk${DTK_SUFFIX}Gui REQUIRED)
find_package(Dtk${DTK_SUFFIX}Widget REQUIRED)

add_executable(myapp
    main.cpp
    mainwindow.cpp
)

target_link_libraries(myapp PRIVATE
    Qt${QT_VERSION_MAJOR}::Core
    Qt${QT_VERSION_MAJOR}::Widgets
    Dtk${DTK_SUFFIX}::Core
    Dtk${DTK_SUFFIX}::Gui
    Dtk${DTK_SUFFIX}::Widget
)
```

### 1.3 使用元包简写

如果已安装 dtkcommon 提供的 `DtkConfig.cmake` 或 `Dtk6Config.cmake`，可用元包一次性引用所有模块：

```cmake
# DTK6 元包
find_package(Dtk6 REQUIRED COMPONENTS Core Gui Widget)
```

### 1.4 CMake 编译依赖（模块级）

| 使用场景 | CMake 依赖 |
|----------|------------|
| 图标系统 (DDciIcon/DIconTheme) | `Dtk6::Gui` |
| 主题/调色板 (DPalette/DGuiApplicationHelper) | `Dtk6::Gui` |
| QWidget 控件 (DDialog/DMainWindow) | `Dtk6::Widget` |
| 配置系统 (DConfig/DSettings) | `Dtk6::Core` |
| 日志系统 (Logger) | `Dtk6::Log` |
| v25 QML 控件 | `Dtk6::Declarative` |
| 文件操作/DBus/DNotify | `Dtk6::Core` |

---

## 2. 头文件引用

### 2.1 标准引用方式

DTK 的公共头文件使用无 `.h` 后缀的转发头，与 CMake target 对应：

```cpp
// 核心模块
#include <DConfig>          // Dtk6::Core
#include <DSettings>        // Dtk6::Core
#include <DStandardPaths>   // Dtk6::Core
#include <DDBusInterface>   // Dtk6::Core
#include <DNotifySender>    // Dtk6::Core

// GUI 模块
#include <DDciIcon>         // Dtk6::Gui
#include <DIconTheme>       // Dtk6::Gui
#include <DPalette>         // Dtk6::Gui
#include <DGuiApplicationHelper>  // Dtk6::Gui

// Widget 模块
#include <DApplication>     // Dtk6::Widget
#include <DDialog>          // Dtk6::Widget
#include <DMainWindow>      // Dtk6::Widget
#include <DTitlebar>        // Dtk6::Widget
#include <DIconButton>      // Dtk6::Widget
```

### 2.2 应用身份、翻译和配置约定

- `applicationName` 通常与可执行文件名一致；不要把显示名称、应用 ID 和单实例 key 混为一个值。
- `DApplication::loadTranslator()` 必须在创建窗口、菜单和其他可翻译对象前调用。
- 翻译文件 basename 应与 `applicationName` 一致；专业单位如 `px` 使用 `QStringLiteral("px")`，不要放入 `tr()`。

### 2.3 日志规范

DTK 应用使用 Qt 自带的日志宏（`qDebug` / `qCInfo` / `qCWarning` 等），不使用 dtklog 的 `dDebug` 宏。dtkcore 提供 `DLogManager` 注册 Appender，应用不需要直接依赖 dtklog，也不需要设置日志路径或格式。

```cpp
#include <DLog>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    // 通过 dtkcore 的 DLogManager 注册日志输出
    DLogManager::registerConsoleAppender();
    DLogManager::registerFileAppender();

    // 使用 Qt 原生日志
    qInfo() << "应用启动";
    qWarning() << "配置未找到，使用默认值";
    qDebug() << "调试信息";
}
```

CMake 依赖：`Dtk6::Core`，**不需要** `Dtk6::Log`。

---

## 3. 最小可运行示例

### 3.1 日志示例

```cpp
#include <QCoreApplication>
#include <DLog>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    DLogManager::registerConsoleAppender();

    qInfo() << "DTK application started";
    return 0;
}
```

CMake 依赖：`Dtk6::Core`。

### 3.2 QWidget 应用（DApplication + DMainWindow）

QWidget 应用**强烈建议**使用 `DApplication` 而非 `QApplication` 初始化，前者在
`QApplication` 基础上额外处理了 DTK 主题、字体、单实例等特性。

```cpp
#include <DApplication>
#include <DMainWindow>
#include <DTitlebar>
#include <DPalette>
#include <DGuiApplicationHelper>

int main(int argc, char *argv[])
{
    DApplication app(argc, argv);

    DMainWindow w;
    w.setMinimumSize(800, 600);
    w.titlebar()->setTitle("My DTK App");
    w.titlebar()->setIcon(DIconTheme::findQIcon("deepin"));
    w.show();

    return app.exec();
}
```

CMake 依赖：`Dtk6::Gui + Dtk6::Widget`。

---

## 4. debian 包依赖

编译依赖放在 `debian/control` 的 `Build-Depends` 中，运行时依赖放在生成包的 `Depends` 中。

### 4.1 编译依赖（Build-Depends）

CMake `find_package` 对应的编译依赖开发包（`-dev`）：

| CMake target | 编译依赖包 |
|-------------|------------|
| `Dtk6::Core` | `libdtk6core-dev` |
| `Dtk6::Gui` | `libdtk6gui-dev` |
| `Dtk6::Widget` | `libdtk6widget-dev` |
| `Dtk6::Declarative` | `libdtk6declarative-dev` |
| `Dtk6::Log` | `libdtk6log-dev` |

### 4.2 运行时依赖（Depends）

QML 模块和共享库对应的运行时包：

| DTK 模块 | 运行时包 |
|----------|---------|
| Core (C++) | `libdtk6core` |
| Gui (C++) | `libdtk6gui` |
| Widget (C++) | `libdtk6widget` |
| Declarative (C++) | `libdtk6declarative` |
| Declarative (QML) | `qml6-module-qtquick-controls2-styles-chameleon` |
| Log (C++) | `libdtk6log` |

### 4.3 debian/control 编写规则

- **C++ 开发包（`-dev`）放在 `Build-Depends` 中**，仅编译时需要
- **共享库包（`libdtk6xxx`）由 `${shlibs:Depends}` 自动推导**，不需要手动写
- **QML 运行时包（`qml6-module-*`）放在 `Depends` 中**，因为 QML 模块不会被 `${shlibs:Depends}` 自动推导
- **dtkdeclarative 的 C++ API 开发包（`libdtk6declarative-dev`）放在 `Build-Depends`**，仅当应用直接使用 dtkdeclarative 的 C++ 头文件时才需要

### 4.4 DTK6 示例

```control
Source: myapp
Build-Depends:
 cmake,
 debhelper-compat (= 13),
 pkg-config,
 qt6-base-dev,
 qt6-tools-dev,
 libdtk6core-dev,
 libdtk6gui-dev,
 libdtk6widget-dev,

Package: myapp
Architecture: any
Depends:
 ${misc:Depends},
 ${shlibs:Depends},
```

如果在 v25 使用 dtkdeclarative QML：

```control
Build-Depends:
 libdtk6declarative-dev,       # 仅当使用 C++ API 时需要

Package: myapp
Architecture: any
Depends:
 qml6-module-qtquick-controls2-styles-chameleon,  # QML 运行时
```

---

## 5. 开发环境初始化检查清单

```bash
# 1. 确认项目源码目录存在
ls <project-path>

# 2. 安装编译依赖
sudo apt build-dep <project-path>

# 3. 确认 CMake 能找到 DTK
cmake --find-package -DNAME=Dtk6Core -DCOMPILER_ID=GNU -DLANGUAGE=C -DMODE=EXIST 2>&1
```
