# org.deepin.dde.LangSelector1 接口参考

该接口提供系统语言选择和切换能力，包括获取区域列表、设置当前区域、添加/删除区域、生成区域、获取区域描述、获取语言包列表、重置语言设置。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.LangSelector1` |
| Object path | `/org/deepin/dde/LangSelector1` |
| Interface | `org.deepin.dde.LangSelector1` |
| Bus | Session |

### 语言选择属性

#### CurrentLocale（属性）

当前区域设置。

- **功能**：当前系统区域设置。
- **触发条件**：属性，当用户切换区域设置时通过 PropertiesChanged 信号通知。
- **使用场景**：控制中心显示当前区域设置。
| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector1 \
  --object-path /org/deepin/dde/LangSelector1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.LangSelector1 CurrentLocale
```

#### Locales（属性）

已安装的区域列表。

- **功能**：已安装的区域列表。
- **触发条件**：属性，当区域安装或卸载时通过 PropertiesChanged 信号通知。
- **使用场景**：控制中心显示已安装的区域列表。
| 属性 | 值 |
|------|------|
| 类型 | `as` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector1 \
  --object-path /org/deepin/dde/LangSelector1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.deepin.dde.LangSelector1 Locales
```

### 语言选择方法

#### GetLocaleList

获取支持的区域列表。

- **功能**：获取所有可用的区域设置列表。
- **触发条件**：当需要展示可选区域列表时调用。
- **使用场景**：控制中心语言和区域选择列表。

- **输入参数**: 无
- **返回值**: `locales`（`a(ss)`，结构体数组）：区域列表（每项为区域名称和描述）

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector1 \
  --object-path /org/deepin/dde/LangSelector1 \
  --method org.deepin.dde.LangSelector1.GetLocaleList
```

#### SetLocale

设置当前区域。

- **功能**：设置当前系统区域。
- **触发条件**：当用户在控制中心选择区域时调用。
- **使用场景**：控制中心区域格式设置。

- **输入参数**: `locale`（string, 类型 `s`）：区域名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector1 \
  --object-path /org/deepin/dde/LangSelector1 \
  --method org.deepin.dde.LangSelector1.SetLocale "zh_CN.UTF-8"
```

#### AddLocale

添加区域。

- **功能**：添加一个区域到已安装区域列表。
- **触发条件**：当用户在控制中心添加新区域时调用。
- **使用场景**：控制中心添加区域。

- **输入参数**: `locale`（string, 类型 `s`）：区域名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector1 \
  --object-path /org/deepin/dde/LangSelector1 \
  --method org.deepin.dde.LangSelector1.AddLocale "en_US.UTF-8"
```

#### DeleteLocale

删除区域。

- **功能**：从已安装区域列表中删除一个区域。
- **触发条件**：当用户在控制中心删除区域时调用。
- **使用场景**：控制中心删除区域。

- **输入参数**: `locale`（string, 类型 `s`）：区域名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector1 \
  --object-path /org/deepin/dde/LangSelector1 \
  --method org.deepin.dde.LangSelector1.DeleteLocale "en_US.UTF-8"
```

#### GenLocale

生成指定区域。

- **功能**：生成指定区域的本地化数据。
- **触发条件**：当用户添加新区域时需要生成对应语言环境数据时调用。
- **使用场景**：区域添加流程中自动生成语言环境数据。

- **输入参数**: `locale`（string, 类型 `s`）：区域名称
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector1 \
  --object-path /org/deepin/dde/LangSelector1 \
  --method org.deepin.dde.LangSelector1.GenLocale "en_US.UTF-8"
```

#### GetLocaleDescription

获取区域的描述信息。

- **功能**：获取指定区域的描述文本。
- **触发条件**：当需要在区域选择列表中展示描述时调用。
- **使用场景**：控制中心区域选择列表显示描述。

- **输入参数**: `locale`（string, 类型 `s`）：区域名称
- **返回值**: `description`（string, 类型 `s`）：区域描述

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector1 \
  --object-path /org/deepin/dde/LangSelector1 \
  --method org.deepin.dde.LangSelector1.GetLocaleDescription "zh_CN.UTF-8"
```

#### GetLanguageSupportPackages

获取指定区域的语言包列表。

- **功能**：获取指定区域对应的语言包列表。
- **触发条件**：当需要查询某区域的语言包安装情况时调用。
- **使用场景**：控制中心语言包管理，检查语言包是否已安装。
- **输入参数**: `locale`（string, 类型 `s`）：区域名称
- **返回值**: `packages`（`as`，string 数组）：语言包列表

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector1 \
  --object-path /org/deepin/dde/LangSelector1 \
  --method org.deepin.dde.LangSelector1.GetLanguageSupportPackages "zh_CN.UTF-8"
```

#### Reset

重置语言设置为默认值。

- **功能**：重置语言和区域设置到默认状态。
- **触发条件**：当用户需要恢复默认语言和区域设置时调用。
- **使用场景**：控制中心语言设置恢复默认。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LangSelector1 \
  --object-path /org/deepin/dde/LangSelector1 \
  --method org.deepin.dde.LangSelector1.Reset
```
