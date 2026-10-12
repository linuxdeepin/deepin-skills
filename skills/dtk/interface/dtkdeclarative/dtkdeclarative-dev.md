# dtkdeclarative-dev

dtkdeclarative 是 DTK 的 QML 声明式控件库，C++ 层能力涵盖 DTK QML 应用的加载、快速渲染、QML 窗口控制和 DTK5 主题兼容，与 org.deepin.dtk QML 模块配合使用，为 DTK 声明式应用提供底层支持。

## 开发包

当前版本使用 DTK6，开发包名为 `libdtk6declarative-dev`。该开发包提供 DTK6 的公开头文件和以下构建入口：

- CMake 包 `Dtk6Declarative` 与导出目标 `Dtk6::Declarative`
- pkg-config 模块 `dtk6declarative`
- qmake 模块 `dtkdeclarative`

仍需维护 DTK5 工程时，使用兼容开发包 `libdtkdeclarative-dev`。它提供 CMake 包 `DtkDeclarative`、导出目标 `Dtk::Declarative`、pkg-config 模块 `dtkdeclarative` 和同名 qmake 模块。

## 集成

### CMake 配置

CMake 是当前推荐的集成方式。DTK6 工程在已有构建目标上查找 `Dtk6Declarative` 并链接 `Dtk6::Declarative`：

```cmake
find_package(Dtk6Declarative REQUIRED)
target_link_libraries(your_target PRIVATE Dtk6::Declarative)
```

`your_target` 替换为使用方工程中的目标名。`Dtk6::Declarative` 会向该目标提供 dtkdeclarative 的头文件搜索路径、链接信息、编译定义和传递依赖，不需要再使用 `include_directories()`、`link_directories()` 或逐项链接 dtkdeclarative 所依赖的库。

仍使用 DTK5 的工程改为查找 `DtkDeclarative` 并链接 `Dtk::Declarative`：

```cmake
find_package(DtkDeclarative REQUIRED)
target_link_libraries(your_target PRIVATE Dtk::Declarative)
```

### 使用方式

构建目标链接 dtkdeclarative 后，可以直接包含所需类型的公开转发头：

```cpp
#include <DAppLoader>
```

也可以包含对应的实际公开头文件，例如 `#include <dapploader.h>`。公开 C++ 类型主要位于 `Dtk::Quick` 命名空间。QML 控件通过 `org.deepin.dtk` QML 模块使用，无需在 C++ 中包含头文件。


---

## 接口分类

- [应用加载](dtkdeclarative-dev/app-loading.md) — 提供 DTK QML 应用的加载器、应用主窗口接口和应用预加载扩展接口
- [快速渲染](dtkdeclarative-dev/fast-rendering.md) — 提供 QML 场景中的帧缓冲区位块传输渲染和视口裁剪渲染能力
- [QML 窗口](dtkdeclarative-dev/qml-window.md) — 提供 DTK 窗口及其附加属性，用于在 QML 场景中控制窗口外观与行为
- [DTK5 主题兼容](dtkdeclarative-dev/dtk5-theme-compat.md) — 提供平台主题代理和系统调色板 QML 项，仅在 DTK5 中提供，DTK6 已移除
