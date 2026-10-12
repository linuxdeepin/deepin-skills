# 辅助登录接口（C）

dde-session-shell 提供 C 语言辅助认证接口，面向需要以 C 函数形式实现厂商密码接收的调用者。该接口通过共享库发布，使用 `extern "C"` 声明，无命名空间，与 C++ 插件接口的集成方式不同。

## 开发包

使用辅助登录接口需安装开发包 `dde-session-shell-dev`。该开发包提供安装在 `dde-session-shell/` 目录下的公开头文件 `assist_login_interface.h`。

## 集成

### CMake 配置

使用辅助登录接口需要链接共享库 `libassist_Login_interface.so`，该库安装于 `/usr/lib/dde-session-shell/modules/` 目录：

```cmake
target_link_libraries(your-plugin PRIVATE /usr/lib/dde-session-shell/modules/libassist_Login_interface.so)
```

### 使用方式

包含头文件：

```cpp
#include <assist_login_interface.h>
```

该接口为 C 语言接口（`extern "C"`），无命名空间。

## 模块API介绍

### assist_login_interface

#### 定位

C 语言辅助认证接口，面向需要以 C 函数形式实现厂商密码接收的调用者。头文件为 `assist_login_interface.h`，无命名空间，使用 `extern "C"` 声明。需链接共享库 `libassist_Login_interface.so`，与 C++ 插件接口的集成方式不同。

#### 功能能力总结

- 向认证服务发送账号和密码进行登录认证，返回发送结果（注意：返回值仅表示发送是否成功，不代表最终认证结果）
- 查询认证服务的运行状态，判断认证服务是否已启动并可用
- 获取非对称加密使用的公钥，供调用方在发送敏感数据前进行加密保护

#### 使用场景

需要实现厂商密码接收插件并通过 C 接口与认证服务交互时。
