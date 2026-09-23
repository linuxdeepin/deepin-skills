# dconfig2cpp 命令参考

DConfig 转 C++ 代码生成器，从 DConfig JSON 配置文件生成 C++ 头文件，将 DConfig 配置项封装为类型安全的 C++ 类。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DCore/bin/dconfig2cpp` |
| DDE 角色 | 开发工具，用于 DConfig 配置项的 C++ 代码生成 |

## 用途

DConfig 转 C++ 代码生成器，从 DConfig JSON 配置文件生成 C++ 头文件，将 DConfig 配置项封装为类型安全的 C++ 类。生成的类包含属性定义、默认值和值变更信号，支持强制请求线程创建 DConfig 实例和禁止生成注释。该工具用于在编译期将 DConfig 配置项静态化，减少运行时 DBus 调用开销。

## 用法

`dconfig2cpp [options] <json-file>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `-c, --class-name <className>` | 生成的类名 | 是 |
| `-o, --output <sourceFile>` | 输出头文件路径（仅头文件） | 是 |
| `--force-request-thread` | 强制请求线程创建 DConfig 实例 | 否 |
| `--no-comment` | 不在生成的代码中生成注释 | 否 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `json-file` | 输入的 DConfig JSON 配置文件路径 |

## 使用示例

```bash
# 从 JSON 配置生成 C++ 头文件
dconfig2cpp -c MyConfig -o myconfig.h config.json

# 生成不含注释的代码
dconfig2cpp -c MyConfig -o myconfig.h --no-comment config.json

# 强制请求线程创建 DConfig 实例
dconfig2cpp -c MyConfig -o myconfig.h --force-request-thread config.json

# 查看帮助信息
dconfig2cpp --help
```
