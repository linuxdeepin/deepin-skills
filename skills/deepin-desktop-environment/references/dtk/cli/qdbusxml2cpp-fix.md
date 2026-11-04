# qdbusxml2cpp-fix 命令参考

DTK 修复版 DBus XML 转 C++ 代码生成器（基于 Qt qdbusxml2cpp 修改）。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix` |
| DDE 角色 | 开发辅助工具，用于从 DBus XML 生成 C++ 适配器和代理代码 |

## 用途

DTK 修复版 DBus XML 转 C++ 代码生成器，基于 Qt 的 `qdbusxml2cpp` 工具修改。读取 DBus 内省 XML 文件，生成实现 DBus 接口的 C++ 代码，包括适配器（adaptor）和代理（proxy）类。与原版相比，此版本增加了对 DTK DBus 扩展的支持（如 `DDBusExtendedAbstractInterface`）。适用于 DTK 项目中 DBus 接口的 C++ 代码自动生成。

## 用法

`qdbusxml2cpp-fix [options...] [xml-or-xml-file] [interfaces...]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-a <filename>` | 将适配器代码写入指定文件 | 是 |
| `-c <classname>` | 指定生成的类名 | 是 |
| `-h` | 显示帮助信息 | 否 |
| `-i <filename>` | 在输出中添加 `#include` 指令 | 是 |
| `-l <classname>` | 生成适配器时，指定父类名 | 是 |
| `-m` | 在 .cpp 文件中生成 `#include "filename.moc"` 语句 | 否 |
| `-N` | 不使用命名空间 | 否 |
| `-p <filename>` | 将代理代码写入指定文件 | 是 |
| `-v` | 输出详细信息 | 否 |
| `-S` | 跳过来自 `types/` 的头文件包含注解 | 否 |
| `-V` | 显示版本信息并退出 | 否 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `xml-or-xml-file` | DBus 内省 XML 内容或 XML 文件路径 |
| `interfaces` | 要生成的接口名列表（可选） |

## 使用示例

```bash
# 从 XML 文件生成适配器和代理代码
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -a myadaptor -p myproxy com.example.Service.xml

# 指定生成的类名
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -c MyAdaptor -a myadaptor com.example.Service.xml

# 指定适配器的父类名
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -a myadaptor -l MyParentClass com.example.Service.xml

# 添加额外的 include 并生成 moc 语句
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -a myadaptor -i mytypes.h -m com.example.Service.xml

# 不使用命名空间
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -N -a myadaptor com.example.Service.xml

# 查看帮助信息
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -h
```
