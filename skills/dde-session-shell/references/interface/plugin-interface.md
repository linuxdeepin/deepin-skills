# 插件接口（C++）

dde-session-shell 提供 C++ 插件接口，用于开发登录认证插件和托盘插件。接口通过公开头文件发布，基于 Qt Plugin 机制加载，包含模块基础接口、V2 登录模块接口、认证回调数据结构和托盘模块接口。C++ 接口仅包含头文件，不需要链接 dde-session-shell 的库文件，使用方编写的插件编译为共享库后由登录器或锁屏器通过 Qt Plugin 机制加载。

## 开发包

使用 C++ 插件接口需安装开发包 `dde-session-shell-dev`。该开发包提供安装在 `dde-session-shell/` 目录下的公开头文件：

- `base_module_interface.h`
- `login_module_interface.h`
- `login_module_interface_v2.h`
- `tray_module_interface.h`

## 集成

### CMake 配置

dde-session-shell 提供 CMake 配置文件 `DdeSessionShellConfig.cmake`，安装到 `lib/cmake/DdeSessionShell` 目录。该配置文件设置 `DDESESSIONSHELL_INCLUDE_DIR` 变量并调用 `include_directories`，不导出库目标。使用方可通过 `find_package` 引入：

```cmake
find_package(DdeSessionShell REQUIRED)
```

作为兼容写法，使用方也可手动指定头文件搜索路径：

```cmake
target_include_directories(your-plugin PRIVATE /usr/include/dde-session-shell)
```

### 使用方式

使用 V2 登录接口时，需同时包含 V1 头文件，因为 V2 通过 `using` 声明引入 V1 中的类型定义：

```cpp
#include <base_module_interface.h>
#include <login_module_interface.h>
#include <login_module_interface_v2.h>
```

开发托盘插件时，包含基础接口和托盘接口头文件：

```cpp
#include <base_module_interface.h>
#include <tray_module_interface.h>
```

C++ 接口类型位于 `dss::module` 和 `dss::module_v2` 命名空间。V2 接口（`login_module_interface_v2.h`）通过 `using` 声明引入以下类型：`AuthResult`、`AuthType`、`AuthState`、`AppType`、`DefaultAuthLevel` 来自 `login_module_interface.h`，`AppDataPtr`、`MessageCallbackFunc` 来自 `base_module_interface.h`。V1 接口本身已过时，但其中定义的类型仍为 V2 所用。

## 模块API介绍

### BaseModuleInterface

#### 定位

所有模块的基础接口，位于 `dss::module` 命名空间，定义于 `base_module_interface.h`。定义模块的初始化、标识、内容和类型，是登录插件和托盘插件的共同基类。

#### 功能能力总结

- 提供插件生命周期初始化入口，由主程序在主线程中调用以完成界面相关的初始化工作，解决插件在非主线程加载时的界面初始化问题
- 为每个插件提供全局唯一标识，用于登录器区分和管理不同模块
- 提供插件要展示的窗口组件，由插件自行管理组件的生命周期
- 声明插件的模块类别（登录型、托盘型、全托管登录型、IPC 辅助登录型、密码扩展登录型），登录器据此决定插件的加载和调用方式
- 控制插件是否被实际加载，支持按平台或架构条件性地启用或禁用插件

#### 使用场景

开发登录插件或托盘插件时，作为插件基类继承。

### LoginModuleInterfaceV2

#### 定位

V2 登录模块接口，位于 `dss::module_v2` 命名空间，定义于 `login_module_interface_v2.h`。替代已过时的 V1 接口，支持认证回调与消息通信。V2 头文件通过 `using` 声明引入 V1 中的类型定义，使用 V2 时需同时包含 `login_module_interface.h` 和 `base_module_interface.h`。V2 头文件还定义了 `AuthCallbackData` 结构体（详见独立章节）和 `AuthObjectType` 枚举。`AuthObjectType` 用于标识验证对象的类型，包括 `LightDM`（lightdm 显示管理器）和 `DeepinAuthenticate`（深度认证框架）两个枚举值。

#### 功能能力总结

- 建立认证结果回调通道，插件在完成认证后将认证结果通过回调函数回传给登录器，该回调在插件初始化前即完成注册
- 支持与登录器进行双向消息通信，插件可接收登录器发送的 JSON 格式消息并返回响应，用于获取插件状态或与登录器同步信息
- 管理登录器回调指针，确保插件在使用回调函数时能正确回传上下文信息，支持多次设置时自动使用最新指针
- 提供插件图标，用于在登录界面中展示插件的视觉标识
- 在认证流程开始前重置插件的界面状态和验证状态，确保每次认证从干净状态开始

#### 使用场景

需要开发登录界面认证插件并使用认证回调时。从 V1 迁移时，改用 V2 接口，实现认证回调注册、图标提供和状态重置核心功能，同时可按需实现消息通信功能以支持与登录器的双向通信。

### AuthCallbackData

#### 定位

认证回调数据结构体，位于 `dss::module_v2` 命名空间，定义于 `login_module_interface_v2.h`。V2 版本使用 `QString` 字段（区别于 V1 中的 `std::string` 版本），作为认证回调函数的参数传递认证结果数据。

#### 功能能力总结

- 封装认证完成后的状态判定结果，包含认证成功、认证失败和无结果三种状态
- 携带认证账户名，供登录器识别通过认证的用户身份
- 携带认证令牌，供登录器完成后续登录会话建立
- 携带面向用户的提示消息，供登录器在界面上展示认证反馈
- 预留 JSON 格式的扩展数据字段，供插件传递超出标准字段的附加认证信息

#### 使用场景

在 V2 登录插件中，认证完成后需要将认证结果回传给登录器时，填充此结构体并通过认证回调函数传递。

### TrayModuleInterface

#### 定位

托盘模块接口，位于 `dss::module` 命名空间，定义于 `tray_module_interface.h`。定义托盘插件需要实现的接口，包括图标、项部件、提示部件和上下文菜单，以及菜单点击响应与消息通信。

#### 功能能力总结

- 提供托盘插件的完整视觉呈现，包括插件图标、托盘项展示组件和悬浮提示组件，用于在登录或锁屏界面的托盘区域展示插件内容
- 支持上下文菜单功能，插件可定义右键菜单内容并响应菜单项的点击事件，实现用户交互操作
- 支持与登录器进行双向消息通信，插件可接收登录器发送的 JSON 格式消息并返回响应，用于获取插件状态或与登录器同步信息
- 管理登录器回调指针，确保插件在使用消息回调函数时能正确回传上下文信息

#### 使用场景

需要开发登录或锁屏界面中的托盘插件时。
