# 插件工厂接口

dde-control-center 提供插件工厂接口，支持第三方开发设置模块插件并集成到控制中心界面框架。插件工厂是第三方插件接入控制中心的入口，负责创建插件主对象并使其 QML 页面能访问插件提供的数据和业务逻辑。框架通过 Qt 插件机制自动加载插件工厂，支持纯 C++ 插件形态，并提供注册宏简化接口实现。

## 开发包

使用 dde-control-center 公开接口前，需要安装开发包 `dde-control-center-dev`。

## 集成

### CMake 配置

CMake 是当前推荐的集成方式。在已有构建目标上查找 `DdeControlCenter` 并链接 `Dde::Control-Center`：

```cmake
find_package(DdeControlCenter REQUIRED)
target_link_libraries(your-plugin PRIVATE Dde::Control-Center)
```

`Dde::Control-Center` 会向该目标提供 dde-control-center 的头文件搜索路径和链接信息，不需要再使用 `include_directories()`、`link_directories()` 或逐项链接依赖库。

开发包还提供以下 CMake 变量：

- `DDE_CONTROL_CENTER_PLUGIN_VERSION`：插件版本（1.1）
- `DDE_CONTROL_CENTER_PLUGIN_DIR`：插件目录名（plugins_v1.1）
- `DDE_CONTROL_CENTER_PLUGIN_INSTALL_DIR`：插件安装完整路径
- `DDE_CONTROL_CENTER_TRANSLATION_INSTALL_DIR`：翻译文件安装路径

### 构建与安装插件

开发包提供以下 CMake 宏用于构建和安装插件：

- `dcc_build_plugin`：构建插件的 QML 模块和 C++ 库，自动处理 QML 资源
- `dcc_install_plugin`：在 `dcc_build_plugin` 基础上将 C++ 库安装到插件目录
- `dcc_handle_plugin_translation`：处理插件翻译，生成并安装 `.ts` 和 `.qm` 翻译文件

插件安装路径为 `${CMAKE_INSTALL_LIBDIR}/dde-control-center/plugins_v1.1/<plugin-name>/`，翻译文件安装路径为 `${CMAKE_INSTALL_DATAROOTDIR}/dde-control-center/translations/v1.1/`。

### 插件注册

插件通过 `DCC_FACTORY_CLASS` 宏注册到控制中心框架。该宏会自动生成一个继承 `dccV25::DccFactory` 的匿名工厂子类，完成 Qt 插件元数据声明（`Q_PLUGIN_METADATA`）和接口注册（`Q_INTERFACES`），并生成 `create()` 方法实例化指定的类。

宏定义如下：

```cpp
DCC_FACTORY_CLASS(classname)
```

- `classname` 是插件的 C++ 主类（通常继承 `QObject`），宏会生成名为 `classname##DccFactory` 的工厂类
- 框架通过 Qt 插件机制自动加载该工厂类，调用其 `create()` 方法获取插件主对象实例

用法示例：

```cpp
#include <dccfactory.h>

class MyModule : public QObject
{
    Q_OBJECT
    // ...
};

DCC_FACTORY_CLASS(MyModule)
```

### 使用方式

在 C++ 源文件中通过以下方式引入公开头文件：

```cpp
#include <dccfactory.h>
```

## 模块API介绍

### DccFactory

#### 定位

控制中心插件工厂接口，是第三方插件接入控制中心框架的入口。

#### 功能能力总结

- 由控制中心框架通过 Qt 插件机制自动加载，负责创建并返回插件主对象，使插件 QML 页面能直接访问插件提供的数据和业务逻辑
- 支持纯 C++ 插件形态，当插件不提供 QML 页面时可直接返回完整的配置对象树
- 提供注册宏自动生成工厂子类，完成 Qt 插件元数据声明和接口注册

#### 使用场景

开发控制中心设置模块插件时，作为插件的入口类使用。适用于需要将自定义设置页面集成到控制中心的场景。
