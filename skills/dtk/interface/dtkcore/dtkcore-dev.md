# dtkcore-dev

dtkcore 是 DTK 的核心基础库，底层能力涵盖配置管理、DBus 通信、DCI 资源与文本处理、文件与路径操作、日志与通知、系统信息与许可、工具与线程，为上层 DTK 模块提供统一的基础设施支撑。

## 开发包

当前版本使用 DTK6，开发包名为 `libdtk6core-dev`。该开发包提供 DTK6 的公开头文件和以下构建入口：

- CMake 包 `Dtk6Core` 与导出目标 `Dtk6::Core`
- pkg-config 模块 `dtk6core`
- qmake 模块 `dtkcore`

仍需维护 DTK5 工程时，使用兼容开发包 `libdtkcore-dev`。它提供 CMake 包 `DtkCore`、导出目标 `Dtk::Core`、pkg-config 模块 `dtkcore` 和同名 qmake 模块。

## 集成

### CMake 配置

CMake 是当前推荐的集成方式。DTK6 工程在已有构建目标上查找 `Dtk6Core` 并链接 `Dtk6::Core`：

```cmake
find_package(Dtk6Core REQUIRED)
target_link_libraries(your_target PRIVATE Dtk6::Core)
```

`your_target` 替换为使用方工程中的目标名。`Dtk6::Core` 会向该目标提供 dtkcore 的头文件搜索路径、链接信息、编译定义和传递依赖，不需要再使用 `include_directories()`、`link_directories()` 或逐项链接 dtkcore 所依赖的库。

仍使用 DTK5 的工程改为查找 `DtkCore` 并链接 `Dtk::Core`：

```cmake
find_package(DtkCore REQUIRED)
target_link_libraries(your_target PRIVATE Dtk::Core)
```

### 使用方式

构建目标链接 dtkcore 后，可以直接包含所需类型的公开转发头：

```cpp
#include <DConfig>
```

也可以包含对应的实际公开头文件，例如 `#include <dconfig.h>`。公开类型主要位于 `Dtk::Core` 命名空间，可使用完整限定名，也可在合适的作用域使用 `DCORE_USE_NAMESPACE`。


---

## 接口分类

- [配置与设置](dtkcore-dev/config-and-settings.md) — 提供统一的配置读写入口、配置缓存与文件访问、配置元信息查询，以及基于后端抽象的设置模型管理，支持分组层级结构与多种持久化后端
- [DBus 通信](dtkcore-dev/dbus-communication.md) — 提供链式 DBus 调用构造、异步方法提交、远端属性读写、扩展接口代理（含属性缓存与批量获取）以及接口导出能力
- [DCI 与文本处理](dtkcore-dev/dci-and-text-processing.md) — 提供 DCI 容器的加载、节点查询与数据读写，文本编码探测与字符集转换，以及安全字符串管理能力
- [文件与路径](dtkcore-dev/file-and-path.md) — 提供文件与目录监视、文件服务、桌面条目解析、标准路径定位、路径拼接工具、回收站操作和最近使用记录管理
- [日志与通知](dtkcore-dev/logging-and-notification.md) — 提供日志规则设置、日志文件定位和桌面通知发送能力
- [系统信息与许可](dtkcore-dev/system-info-and-license.md) — 提供发行版、产品、组织、架构及硬件运行状态查询，应用标识查询，以及组件级许可信息读取能力
- [工具与线程](dtkcore-dev/tools-and-threading.md) — 提供单位换算与格式化、线程投递、单例基类模板、对象基类、虚函数表操作以及路径拼接工具
