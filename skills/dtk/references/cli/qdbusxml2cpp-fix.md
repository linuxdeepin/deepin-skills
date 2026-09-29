# qdbusxml2cpp-fix 命令参考

D-Bus XML 转 C++ 代码生成器，是 Qt 自带 `qdbusxml2cpp` 的增强版本。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix` |
| DDE 角色 | 开发工具，用于 D-Bus 接口 C++ 代码生成 |

## 用途

D-Bus XML 转 C++ 代码生成器，是 Qt 自带 `qdbusxml2cpp` 的增强版本。从 D-Bus introspection XML 文件生成适配器（adaptor）或代理（proxy）的 C++ 代码，支持自动包含 `DDBusExtendedAbstractInterface` 头文件、跳过命名空间、跳过 include 注解增强功能。该工具用于 DTK D-Bus 接口的代码生成。

## 用法

`qdbusxml2cpp-fix [options...] [xml-or-xml-file] [interfaces...]`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-V` | 显示程序版本并退出 | 否 |
| `-a <filename>` | 将适配器代码写入指定文件 | 是 |
| `-c <classname>` | 指定生成的类名 | 是 |
| `-i <filename>` | 在输出中添加 `#include` | 是 |
| `-l <classname>` | 生成适配器时指定父类名 | 是 |
| `-m` | 在 .cpp 文件中生成 `#include "filename.moc"` 语句 | 否 |
| `-N` | 不使用命名空间 | 否 |
| `-p <filename>` | 将代理代码写入指定文件 | 是 |
| `-v` | 显示详细输出 | 否 |
| `-S` | 跳过来自 `types/` 的 include 注解头文件 | 否 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `xml-or-xml-file` | 输入的 D-Bus introspection XML 内容或文件路径 |
| `interfaces` | 要生成的接口名列表 |

## 使用示例

```bash
# 从 XML 文件生成代理代码
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -p myproxy com.example.MyService.xml

# 从 XML 文件生成适配器代码
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -a myadaptor com.example.MyService.xml

# 指定类名生成代理代码
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -c MyServiceProxy -p myproxy com.example.MyService.xml

# 生成适配器代码并指定父类
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -a myadaptor -l QObject com.example.MyService.xml

# 跳过命名空间
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -N -p myproxy com.example.MyService.xml

# 跳过 types/ 目录的 include 注解
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -S -p myproxy com.example.MyService.xml

# 查看帮助信息
/usr/libexec/dtk6/DCore/bin/qdbusxml2cpp-fix -h
```
