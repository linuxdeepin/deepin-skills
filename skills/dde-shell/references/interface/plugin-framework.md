# 插件框架接口

dde-shell 提供三层插件模型（Applet、Containment、Panel）、插件元数据与实例数据、插件发现与加载、跨插件通信桥接和子插件项模型暴露，是第三方开发 dde-shell 插件的 C++ 基础接口。插件通过元数据描述自身身份与入口，框架在运行时发现并加载插件，通过插件加载器构建插件树，通过桥接机制实现插件间通信。

## 开发包

使用 dde-shell 框架公开接口前，需要安装开发包 `libdde-shell-dev`。

## 集成

### CMake 配置

CMake 是当前推荐的集成方式。在已有构建目标上查找 `DDEShell` 并链接 `Dde::Shell`：

```cmake
find_package(DDEShell REQUIRED)
target_link_libraries(your-plugin PRIVATE Dde::Shell)
```

`Dde::Shell` 会向该目标提供 dde-shell 的头文件搜索路径和链接信息，不需要再使用 `include_directories()`、`link_directories()` 或逐项链接依赖库。

开发包还提供以下 CMake 变量：

- `DDE_SHELL_PACKAGE_INSTALL_DIR`：插件包资源安装路径（`share/dde-shell/`）
- `DDE_SHELL_PLUGIN_INSTALL_DIR`：插件库安装路径（`lib/dde-shell/`）
- `DDE_SHELL_TRANSLATION_INSTALL_DIR`：翻译文件安装路径（`share/dde-shell/`）

### 构建与安装插件

开发包提供以下 CMake 宏用于插件包管理：

- `ds_install_package(PACKAGE <id> [TARGET <lib>])`：构建并安装插件包，将 package/ 目录资源安装到包安装目录，可选将库文件安装到插件库目录
- `ds_build_package(PACKAGE <id> [TARGET <lib>])`：构建插件包（不安装），将 package/ 目录拷贝到构建目录
- `ds_handle_package_translation(PACKAGE <id>)`：自动扫描 QML 和 C++ 源文件生成翻译并安装

插件包资源安装路径为 `share/dde-shell/`，插件库安装路径为 `lib/dde-shell/`，翻译文件安装路径为 `share/dde-shell/<plugin-id>/translations/`。

### 插件注册

插件通过 `D_APPLET_CLASS` 宏注册到 dde-shell 框架。该宏会自动生成一个带有 `Q_PLUGIN_METADATA` 和 `Q_INTERFACES` 声明的匿名工厂子类，完成 Qt 插件注册。

宏定义如下：

```cpp
D_APPLET_CLASS(classname)
```

- `classname` 是插件的 C++ 主类（通常继承 `DApplet`），宏会生成对应的工厂类
- 框架通过 Qt 插件机制自动加载该工厂类，创建插件实例

用法示例：

```cpp
#include <pluginfactory.h>

class MyPlugin : public DApplet
{
    Q_OBJECT
    // ...
};

D_APPLET_CLASS(MyPlugin)
```

### 使用方式

构建目标链接 dde-shell 后，可以直接包含所需类型的公开头文件。链接 `dde-shell-frame` 后头文件搜索路径已配置完成，无需 `dde-shell/` 前缀，直接包含即可：

```cpp
#include <applet.h>
```

公开类型位于 `ds` 命名空间（`DS_NAMESPACE`），可使用完整限定名，也可在合适的作用域使用 `DS_USE_NAMESPACE` 引入。

## 模块API介绍

### DApplet

#### 定位

基础功能部件插件类型，所有 Applet 插件的基类，定义插件的生命周期阶段和基本属性。

#### 功能能力总结

- 管理插件完整生命周期：从构造开始，依次经历加载阶段（从 DConfig 或实例数据读取配置）和初始化阶段（建立信号连接、创建 UI），最终进入就绪状态
- 提供插件身份标识，包括实例 ID 和插件 ID，用于在整个插件树中唯一定位该插件实例
- 持有 QML 根对象的引用，使 C++ 层能够访问和操作插件在 QML 中创建的 UI 元素
- 维护插件实例数据，支持在运行时更新插件数据内容
- 通过元数据关联插件与 `metadata.json` 的描述信息，包括插件 ID、入口 URL、父插件信息

#### 使用场景

开发基础功能部件插件时，作为插件基类继承。

### DContainment

#### 定位

容器插件类型，继承自 DApplet，管理子 Applet，提供子插件数据列表和添加子 Applet 的能力。

#### 功能能力总结

- 以层级结构管理子插件实例，支持根据插件数据动态创建子 Applet 并将其纳入容器管理
- 提供子插件列表的查询能力，可获取全部子插件实例或按实例 ID 精确查找特定子插件
- 支持移除子插件实例，实现插件树结构的动态调整
- 将子 Applet 的 QML 视图项通过标准模型暴露给 QML 视图层，供 Repeater 类型视图组件渲染

#### 使用场景

开发需要包含子插件的容器插件时。

### DPanel

#### 定位

顶级面板插件类型，继承自 DContainment，管理窗口，提供主窗口和弹出窗口的访问能力。

#### 功能能力总结

- 管理面板的主窗口，作为整个面板的顶层显示容器
- 提供弹出窗口、提示窗口和菜单窗口的创建与访问能力，支持面板插件在不同交互场景下显示对应的浮层窗口
- 继承容器的子插件管理能力，作为面板内所有子插件的根容器
- 通过 QML 附加属性机制，使面板内子插件能够访问所属面板的窗口资源

#### 使用场景

开发 Dock、顶栏这类顶级面板插件时。

### DPluginLoader

#### 定位

插件发现与加载单例，负责从安装目录发现和加载插件。

#### 功能能力总结

- 从配置的插件目录中发现所有已安装的插件元数据，支持动态添加插件搜索目录
- 管理已禁用插件列表，支持在加载阶段跳过被禁用的插件
- 提供插件元数据查询能力，可按插件 ID 查询父插件、子插件列表，以及获取根插件和全部插件列表
- 根据插件元数据和实例数据创建插件实例，完成从元数据描述到运行时实例的转化

#### 使用场景

需要查询已安装插件的元数据信息时。

### DAppletBridge

#### 定位

跨插件通信桥接类型，用于查找并访问其他插件实例。

#### 功能能力总结

- 以目标插件 ID 为索引，在已加载的插件树中查找对应的插件实例，并判断目标插件是否已成功加载
- 为目标插件实例创建代理对象，使调用方能够以属性读写和方法调用的方式与目标插件交互，而无需直接持有目标实例的引用
- 支持同时获取目标插件的所有实例代理（当一个插件 ID 对应多个实例时）和单个实例代理

#### 使用场景

需要在插件之间通信、读取其他插件属性或调用其他插件方法时。

### DPluginMetaData

#### 定位

插件元数据类型，来自 `metadata.json` 文件，描述插件的 ID、版本、入口和父子关系。

#### 功能能力总结

- 封装插件元数据的完整描述信息，包括插件 ID、插件目录路径和 QML 入口文件 URL
- 支持以键值对方式查询元数据中的任意自定义字段，为插件提供灵活的元数据扩展读取能力
- 提供从 JSON 文件和 JSON 字符串加载元数据的能力，并支持识别根插件

#### 使用场景

需要读取插件元数据信息时。

### DAppletData

#### 定位

插件实例运行时数据类型，保存插件实例在运行时的数据。

#### 功能能力总结

- 承载插件实例的运行时标识信息，包括实例 ID 和插件 ID，用于区分同一插件的多个实例
- 管理子插件实例的数据列表，以树形结构组织插件实例之间的父子关系
- 支持从插件元数据和 QVariantMap 构造实例数据，并可将实例数据转换为 QVariantMap 进行传递

#### 使用场景

需要构造或修改插件实例数据时。

### DAppletItemModel

#### 定位

子 Applet 项模型类型，将子 Applet 的 QML item 暴露给 QML 视图。

#### 功能能力总结

- 作为标准列表模型，维护容器内所有子 Applet 的 QML 根对象列表
- 支持动态添加和移除子插件项，实时反映容器中子插件的变化
- 为 QML 视图层提供符合 QAbstractListModel 接口的数据访问能力，使 Repeater、ListView 类型视图组件能够直接渲染子插件的 UI 元素

#### 使用场景

需要在 QML 中使用 Repeater 渲染子 Applet item 时。
