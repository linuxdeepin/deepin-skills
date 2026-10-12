# Dock 接口

dde-shell 提供 Dock 面板插件接口与 Dock 项信息结构体，用于第三方开发 Dock 面板插件和通过 D-Bus 通信传递 Dock 项显示信息。Dock 接口在框架插件接口基础上扩展 Dock 面板的可见性控制、支持状态查询和 Dock 项信息统一访问能力。

## 开发包

使用 Dock 面板公开接口前，需要安装开发包 `libdde-shell-dock-dev`。该开发包会自动引入对 `libdde-shell-dev` 的依赖，因此无需单独安装框架开发包。

## 集成

### CMake 配置

在已有构建目标上查找 `DDEShellDock` 并链接 `Dde::ShellDock`：

```cmake
find_package(DDEShellDock REQUIRED)
target_link_libraries(your-plugin PRIVATE Dde::ShellDock)
```

`Dde::ShellDock` 会向该目标提供 Dock 头文件搜索路径和链接信息。`DDEShellDockConfig.cmake` 内部会自动调用 `find_dependency(DDEShell)`，因此查找 DDEShellDock 即可同时获得 `Dde::Shell` 的传递依赖。如需在同一个目标中使用框架类型，可将 `Dde::Shell` 一并链接：

```cmake
target_link_libraries(your-plugin PRIVATE Dde::Shell Dde::ShellDock)
```

### 使用方式

构建目标链接 dde-shell Dock 后，可以直接包含所需类型的公开头文件。链接 `dde-shell-frame` 后头文件搜索路径已配置完成，Dock 相关头文件在 `dock/` 子目录下，直接包含即可：

```cpp
#include <dock/dappletdock.h>
```

## 模块API介绍

### DAppletDock

#### 定位

Dock 面板插件接口类型，继承自 DApplet，提供 Dock 面板的可见性控制、支持状态查询和 Dock 项信息获取能力。

#### 功能能力总结

- 管理 Dock 面板的显示与隐藏状态，支持在运行时动态切换 Dock 的可见性，并在状态变化时通过信号通知相关组件
- 维护 Dock 功能的支持状态，标识当前环境下 Dock 是否可用（如某些设备不支持 Dock 功能），并在支持状态变化时发出通知
- 提供 Dock 项信息的统一访问接口，使 Dock 插件能够以标准化的数据结构向外部暴露自身的名称、显示名称、图标、标识键、设置键和可见状态

#### 使用场景

开发需要访问 Dock 面板可见性状态或 Dock 项信息的插件时。

### DockItemInfo

#### 定位

Dock 项信息结构体，描述 Dock 区域插件项的名称、显示名称、标识键、设置键、图标和可见性，已注册为 Qt 元类型和 D-Bus 可序列化类型。

#### 功能能力总结

- 以结构化数据描述 Dock 插件项的完整显示信息，包括插件名称、用户可见的显示名称、唯一标识键、设置键和控制中心图标路径
- 包含可见性状态字段，标识该 Dock 项是否在任务栏中显示
- 支持 D-Bus 序列化和反序列化，使 Dock 项信息能够通过 D-Bus 通信在进程间传递

#### 使用场景

需要在 D-Bus 通信中传输 Dock 项信息，或读取 Dock 插件项的显示信息时。
