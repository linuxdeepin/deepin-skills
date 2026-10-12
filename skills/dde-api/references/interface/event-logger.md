# 事件日志接口

dde-api 提供 header-only C++ 事件日志记录接口，主要符号位于 `DDE_EventLogger` 命名空间下。调用者通过 `EventLogger` 单例将事件日志序列化为 JSON 并发送到后端库完成写入，通过 `EventLoggerData` 结构组装日志内容。

## 开发包

- `dde-api-dev`：提供公开头文件 `dde-api/eventlogger.hpp` 和 CMake 配置文件 `DDEAPIConfig.cmake`

## 集成

### CMake 配置

使用 `find_package` 查找 CMake 配置，通过 `target_link_libraries` 链接导出目标获取头文件搜索路径：

```cmake
find_package(DDEAPI QUIET)
if(DDEAPI_FOUND)
    target_link_libraries(myapp PRIVATE DDEAPI::EventLogger)
endif()
```

`DDEAPI::EventLogger` 是 INTERFACE IMPORTED 目标，仅传递头文件包含路径，不引入实际链接库。

### 使用方式

在源文件中包含公开头文件，使用 `DDE_EventLogger` 命名空间访问公开符号：

```cpp
#include <dde-api/eventlogger.hpp>
using namespace DDE_EventLogger;
```

## 模块API介绍

### EventLogger

#### 定位

C++ header-only 事件日志记录接口，以单例方式提供全局唯一的日志记录器实例，面向需要将事件日志发送到后端的调用者。

#### 功能能力总结

- 提供事件日志的记录与上报能力，以单例方式运行，确保全局唯一实例并保证多线程环境下的写入安全
- 调用者组装日志数据后，日志记录器将数据序列化为 JSON 格式的紧凑字符串，通过动态加载的事件日志后端库完成实际写入
- 后端库在首次写入时自动以当前应用标识完成初始化，调用者无需关心底层通信细节
- 日志写入前自动检测当前系统版本是否启用事件日志功能，社区版系统下静默跳过写入以避免不必要的性能开销
- 提供独立的事件日志启用检测函数，调用者可在组装日志数据前主动检测系统版本，以决定是否执行后续日志构造逻辑
- 整个接口为 header-only 形式，仅需包含头文件即可使用，无需链接额外库文件

#### 使用场景

需要在 C++ 程序中记录并发送事件日志时使用。当需要根据系统版本条件性地记录日志时，可先检测当前版本是否启用事件日志功能，再决定是否执行日志构造与写入。

### EventLoggerData

#### 定位

事件日志数据结构，用于描述单条事件日志的内容，作为 `EventLogger` 写入日志时的参数载体。

#### 功能能力总结

- 描述单条事件日志的完整内容，由线程上下文标识、目标对象标识和结构化消息体三部分组成
- 线程上下文标识用于关联产生日志的线程
- 目标对象标识指明日志所关注的目标对象
- 消息体以 JSON 对象形式承载任意结构化的事件详情，支持灵活扩展自定义字段
- 支持默认构造与赋值操作，便于调用者在不同场景下按需组装日志内容后传递给日志记录器

#### 使用场景

在写入事件日志前构造该结构，填入线程标识、目标对象标识和消息内容，传递给日志记录器实例完成日志写入。
