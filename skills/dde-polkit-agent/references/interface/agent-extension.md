# 认证代理扩展接口

dde-polkit-agent 提供认证代理扩展接口，允许第三方通过继承 `dpa::AgentExtension` 接口实现自定义认证逻辑，通过 `dpa::AgentExtensionProxy` 接口获取当前认证会话的上下文信息。扩展插件编译为共享库，由认证代理通过 Qt Plugin 机制在运行时加载。

## 开发包

使用方需安装开发包 `dde-polkit-agent-dev`。该开发包提供以下公开头文件，安装于系统头文件目录的 `dpa/` 子目录下：

- `agent-extension.h`
- `agent-extension-proxy.h`

## 集成

### CMake 配置

dde-polkit-agent 不导出 CMake 配置文件或库目标，使用方无需调用 `find_package`。在 CMake 工程中手动指定头文件搜索路径，并链接 Qt 插件机制所需的模块：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core Widgets)
target_include_directories(your-plugin PRIVATE /usr/include/dpa)
```

扩展插件编译为共享库（`SHARED`），由 dde-polkit-agent 通过 `QPluginLoader` 在运行时加载，使用方无需链接 dde-polkit-agent 的库文件。

### 构建与安装插件

扩展插件共享库（`.so`）需要安装到 dde-polkit-agent 的插件搜索路径下才能被加载。默认搜索路径为 `/usr/lib/polkit-1-dde/plugins/`。也可以通过环境变量 `DDE_POLKIT_AGENT_PLUGINS_DIRS` 指定额外的插件搜索目录，多个目录以路径分隔符分隔。

```cmake
install(TARGETS your-plugin LIBRARY DESTINATION /usr/lib/polkit-1-dde/plugins)
```

### 插件注册

扩展插件使用 Qt Plugin 机制接入 dde-polkit-agent。插件 IID 定义在 `agent-extension.h` 中，宏为 `AgentExtensionPluginIID`，值为 `com.deepin.dpa.AgentExtension`。

使用方在插件类声明中使用 `Q_PLUGIN_METADATA` 宏声明此 IID，并通过 `FILE` 参数指定 JSON 元数据文件。`agent-extension.h` 中已通过 `Q_DECLARE_INTERFACE` 注册接口与 IID 的关联，使用方在插件类中通过 `Q_INTERFACES(dpa::AgentExtension)` 声明实现该接口。

元数据文件中必须声明 `api_version` 字段，值为 `"1.0"`，否则插件不会被加载。元数据文件示例（`plugin.json`）：

```json
{
    "api_version": "1.0"
}
```

插件类声明示例：

```cpp
class MyExtension : public QObject, public dpa::AgentExtension
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID AgentExtensionPluginIID FILE "plugin.json")
    Q_INTERFACES(dpa::AgentExtension)
    // ...
};
```

### 使用方式

在源文件中包含所需类型的公开头文件：

```cpp
#include <agent-extension.h>
#include <agent-extension-proxy.h>
```

公开类型位于 `dpa` 命名空间。

## 模块API介绍

### AgentExtension

#### 定位

认证代理扩展接口，面向需要自定义认证行为的调用者。调用者通过继承此接口并实现全部纯虚方法，将自定义认证逻辑接入 dde-polkit-agent。插件类需要声明 `Q_PLUGIN_METADATA(IID AgentExtensionPluginIID)` 和 `Q_INTERFACES(dpa::AgentExtension)`，使 `QPluginLoader` 能够识别并实例化插件对象。

#### 功能能力总结

- 扩展生命周期管理：在认证代理加载扩展时通过代理对象获取当前认证会话的上下文信息（动作 ID、用户名、密码），完成初始化准备；在认证流程结束或扩展卸载时释放所占用的资源
- 认证动作过滤：扩展声明自身关注的 Polkit 认证动作 ID 列表，认证代理仅在遇到匹配的动作时激活该扩展；若列表为空则对所有认证动作生效，实现精准或全局的认证行为扩展
- 风险提示展示：向用户展示扩展功能的描述信息，在认证对话框中呈现潜在风险说明，帮助用户在执行提权操作前了解扩展将执行的操作内容
- 用户交互选项：在认证对话框中提供一组可选择的按钮选项，使用户能够在多种认证或验证方式之间进行选择，由认证代理将选项按钮集成到对话框界面中
- 自定义认证执行：在用户确认选择后，扩展执行自定义的认证或验证逻辑，可通过代理对象获取当前认证会话的用户名和密码，将自定义认证流程接入 dde-polkit-agent

#### 使用场景

需要为特定 Polkit 认证动作添加自定义认证逻辑时，继承 `AgentExtension` 实现扩展插件，为提权操作添加额外的认证选项按钮供用户选择，并在用户确认后执行自定义的认证或验证流程。

### AgentExtensionProxy

#### 定位

扩展代理接口，面向已注册的扩展插件，提供获取当前认证上下文信息的能力。在扩展初始化时传入此接口的实例，插件后续通过该实例读取当前认证会话的相关信息。

#### 功能能力总结

- 提供当前认证动作的标识信息，使扩展能够识别触发认证的具体 Polkit 动作，并据此决定是否执行特定的认证流程或差异化逻辑
- 提供当前认证的用户名，使扩展能够针对特定用户执行差异化的认证逻辑或查询用户相关的认证凭据
- 提供用户在认证对话框中输入的密码，使扩展能够在自定义认证流程中复用该密码，例如将其传递给外部认证服务或进行二次验证

#### 使用场景

扩展插件需要获取当前认证动作 ID、用户名或密码时，通过初始化时传入的代理对象读取所需信息，用于判断是否执行特定的认证流程或完成自定义认证操作。
