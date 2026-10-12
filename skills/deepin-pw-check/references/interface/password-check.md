# 密码校验接口

deepin-pw-check 提供密码复杂度校验、密码强度等级评估、密码校验策略查询、错误码到可读信息转换和调试日志控制能力。公开头文件为 `deepin_pw_check.h`，安装在 `/usr/include/` 目录下。

## 开发包

使用方需安装开发包 `libdeepin-pw-check-dev`，该包提供以下内容：

- 公开头文件 `deepin_pw_check.h`，安装路径为 `/usr/include/`。
- 动态链接库 `libdeepin_pw_check.so` 和静态链接库 `libdeepin_pw_check.a`。
- pkg-config 元数据文件 `libdeepin_pw_check.pc`，包名为 `deepin_pw_check`。

## 集成

### CMake 配置

deepin-pw-check 提供 pkg-config 元数据，使用方在 CMake 工程中通过 `PkgConfig` 模块查找并链接：

```cmake
find_package(PkgConfig REQUIRED)
pkg_check_modules(DEEPIN_PW_CHECK REQUIRED deepin_pw_check)

target_link_libraries(your_target PRIVATE ${DEEPIN_PW_CHECK_LIBRARIES})
```

`your_target` 替换为使用方工程中的目标名。`pkg_check_modules` 会自动解析头文件搜索路径和链接库路径，无需额外设置 `target_include_directories`。

在不使用 pkg-config 的环境中，可通过 `find_path` 和 `find_library` 手动查找头文件和库：

```cmake
find_path(DEEPIN_PW_CHECK_INCLUDE_DIR deepin_pw_check.h)
find_library(DEEPIN_PW_CHECK_LIB deepin_pw_check)

target_include_directories(your_target PRIVATE ${DEEPIN_PW_CHECK_INCLUDE_DIR})
target_link_libraries(your_target PRIVATE ${DEEPIN_PW_CHECK_LIB})
```

### 使用方式

构建目标链接 deepin-pw-check 后，在源文件中包含公开头文件即可使用全部公开接口：

```c
#include <deepin_pw_check.h>
```

## 模块API介绍

### deepin_pw_check.h

#### 定位

密码校验核心接口，面向需要在 C 或 C++ 程序中执行密码复杂度校验、强度等级评估、策略参数查询和错误码转换的调用者。接口分为普通版和 grub2 版两组，普通版读取 `/etc/deepin/dde.conf` 配置，grub2 版读取 `/etc/deepin/grub2_edit_auth.conf` 配置。

#### 功能能力总结

- **密码复杂度校验**：根据配置文件中定义的密码策略对密码进行全面校验，依次检查密码是否为空、长度是否在允许范围内、首字母是否大写（如策略启用）、密码是否与用户名相同（在密码长度不小于 8 且字符类型数不小于 3 时）、字符是否均属于允许的字符集（拒绝中文字符）、字符类型数量是否达到最低要求、是否包含超过阈值的回文子串、是否匹配字典中的常见单词（基于 cracklib）、是否包含单调递增或递减的字符序列（包括键盘相邻按键序列）、是否包含连续相同字符。校验通过返回成功码，任一环节不通过则返回对应的错误码，调用者无需自行实现校验逻辑。普通版和 grub2 版分别使用各自的配置文件，互不干扰。
- **密码强度等级评估**：综合密码长度和包含的字符类型数量（大写字母、小写字母、数字、特殊字符），结合配置文件中定义的强度阈值，将密码强度划分为错误、低、中、高四个等级，供调用方根据强度等级进行界面提示或策略决策。普通版和 grub2 版各自读取对应配置文件中的阈值。
- **密码校验策略查询**：从配置文件中读取当前生效的密码校验策略参数，包括密码最小长度、最大长度、最小字符类型数、允许的字符集策略、回文检查位数、单调字符检查位数、连续相同字符检查位数。调用方可在校验前展示当前策略要求，或在校验失败时结合策略参数生成更具体的提示。普通版和 grub2 版分别查询各自的配置文件。
- **错误码到可读信息转换**：将密码校验返回的错误码转换为面向最终用户的本地化可读提示字符串，部分提示会动态拼接当前配置中的实际策略参数（如最小长度、最小字符类型数），使提示信息更加具体。普通版和 grub2 版分别使用各自的配置文件生成提示。
- **调试控制**：通过设置全局调试标志，控制库内部是否输出包含源文件名、函数名和行号的调试日志，便于开发阶段排查密码校验流程问题。
- **校验模式与类型定义**：提供标准校验和严格校验两种模式宏定义，标准模式仅检查长度和字符有效性，严格模式额外检查字典词和回文；定义了涵盖全部密码校验结果的错误码枚举（1 个成功码加 15 个错误码）和四级密码强度等级枚举，作为校验和评估功能的统一返回类型。

> **注意**：密码复杂度校验和策略查询接口中的校验级别参数在头文件中已标注为废弃，保留仅为向后兼容，实际校验行为由配置文件中的策略参数决定。

#### 使用场景

需要在 C 或 C++ 程序中校验密码复杂度、评估密码强度等级、查询密码校验策略配置、将错误码转换为可读信息、执行 grub2 密码校验或控制调试输出时。
