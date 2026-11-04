# dconfig2cpp 命令参考

DConfig JSON 配置文件转 C++ 类代码生成器。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DCore/bin/dconfig2cpp` |
| DDE 角色 | 开发辅助工具，用于从 DConfig JSON 配置自动生成 C++ 类代码 |

## 用途

DConfig JSON 配置文件转 C++ 类代码生成器。读取 DConfig 的 JSON 配置文件，自动生成对应的 C++ 头文件类代码，封装配置项的读写操作。生成的类提供类型安全的属性访问器、默认值管理和变更信号，简化 DConfig 配置在 C++ 项目中的集成。适用于使用 DTK DConfig 模块的应用开发。

## 用法

`dconfig2cpp [options] <json-file>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `-c, --class-name <className>` | 指定生成的 C++ 类名 | 是 |
| `-o, --output <sourceFile>` | 指定输出的头文件路径（header only） | 是 |
| `--force-request-thread` | 强制在请求线程中创建 DConfig 实例 | 否 |
| `--no-comment` | 不在生成的代码中生成注释 | 否 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `json-file` | 输入的 DConfig JSON 配置文件路径 |

## 使用示例

```bash
# 从 JSON 配置生成指定类名的 C++ 代码
/usr/libexec/dtk6/DCore/bin/dconfig2cpp -c MySettings -o mysettings.h org.example.MySettings.json

# 生成不含注释的代码
/usr/libexec/dtk6/DCore/bin/dconfig2cpp -c MySettings -o mysettings.h --no-comment org.example.MySettings.json

# 强制在请求线程中创建 DConfig 实例
/usr/libexec/dtk6/DCore/bin/dconfig2cpp -c MySettings -o mysettings.h --force-request-thread org.example.MySettings.json

# 查看帮助信息
/usr/libexec/dtk6/DCore/bin/dconfig2cpp --help
```
