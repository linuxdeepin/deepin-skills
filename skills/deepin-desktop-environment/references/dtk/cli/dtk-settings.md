# dtk-settings 命令参考

DTK 设置翻译代码生成工具，从 JSON 配置生成翻译 C++ 代码和 GSettings schema。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属 DTK | DTK 开发工具集 |
| 安装路径 | `/usr/libexec/dtk6/DCore/bin/dtk-settings` |
| DDE 角色 | 开发辅助工具，用于从 DTK 设置 JSON 配置生成翻译代码和 GSettings schema |

## 用途

DTK 设置翻译代码生成工具。读取 DTK Settings 的 JSON 配置文件，提取其中需要翻译的字符串（组名、选项名、选项文本、选项项列表），生成包含 `QObject::tr()` 调用的 C++ 翻译代码。同时支持生成 GSettings 的 XML schema 文件，将 DTK Settings 配置映射为 GSettings 兼容的格式。适用于 DTK 应用中设置界面的国际化翻译和 GSettings 集成开发。

## 用法

`dtk-settings [options] <json-file>`

## 参数

| 选项 | 说明 | 是否需要值 |
|------|------|------------|
| `-h, --help` | 显示命令行帮助 | 否 |
| `-v, --version` | 显示版本信息 | 否 |
| `-g, --gsettings <xml-file>` | 生成 GSettings schema XML 文件 | 是 |
| `-o, --output <cpp-file>` | 指定输出的 C++ 翻译代码文件 | 是 |

## 位置参数

| 参数 | 说明 |
|------|------|
| `json-file` | DTK Settings 的 JSON 配置文件路径 |

## 使用示例

```bash
# 生成翻译 C++ 代码文件
/usr/libexec/dtk6/DCore/bin/dtk-settings -o settings_translate.cpp settings.json

# 生成 GSettings schema XML 文件
/usr/libexec/dtk6/DCore/bin/dtk-settings -g org.example.settings.gschema.xml settings.json

# 同时生成翻译代码和 GSettings schema
/usr/libexec/dtk6/DCore/bin/dtk-settings -o settings_translate.cpp -g org.example.settings.gschema.xml settings.json

# 查看帮助信息
/usr/libexec/dtk6/DCore/bin/dtk-settings --help
```
