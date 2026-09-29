# dtk-settings 命令参考

DTK 设置工具，用于从 DTK 设置 JSON 配置文件生成翻译代码（C++）和 GSettings schema（XML）。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DCore/bin/dtk-settings` |
| DDE 角色 | 开发调试工具，用于 DTK 设置项翻译代码和 GSettings schema 生成 |

## 用途

DTK 设置工具，用于从 DTK 设置 JSON 配置文件生成翻译代码（C++）和 GSettings schema（XML）。它解析 DTK Settings 的 JSON 描述文件，提取所有设置项的名称、文本和选项列表，生成包含 `QObject::tr()` 调用的 C++ 代码文件用于国际化翻译；也可以将设置项转换为 GSettings 兼容的 XML schema 文件。该工具是 DTK 应用设置开发和打包流程中的辅助工具。

## 用法

`dtk-settings [options] <json-file>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `-g, --gsettings <xml-file>` | 生成 GSettings schema XML 文件 | 是 |
| `-o, --output <cpp-file>` | 输出翻译 C++ 文件 | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `json-file` | DTK Settings JSON 描述配置文件 |

## 使用示例

```bash
# 从 JSON 配置生成翻译 C++ 代码
/usr/libexec/dtk6/DCore/bin/dtk-settings -o settings_translate.cpp config.json

# 从 JSON 配置生成 GSettings schema XML
/usr/libexec/dtk6/DCore/bin/dtk-settings -g schema.xml config.json

# 同时生成翻译代码和 GSettings schema
/usr/libexec/dtk6/DCore/bin/dtk-settings -o settings_translate.cpp -g schema.xml config.json

# 查看帮助信息
/usr/libexec/dtk6/DCore/bin/dtk-settings --help
```
