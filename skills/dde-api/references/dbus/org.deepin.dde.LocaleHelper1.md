# org.deepin.dde.LocaleHelper1 接口参考

该接口提供系统区域设置生成和切换能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.LocaleHelper1` |
| Object path | `/org/deepin/dde/LocaleHelper1` |
| Interface | `org.deepin.dde.LocaleHelper1` |
| Bus | System |


### 区域设置方法

#### SetLocale

设置系统区域。

- **输入参数**: `locale`（string, 类型 `s`）：区域名称
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.LocaleHelper1 \
  --object-path /org/deepin/dde/LocaleHelper1 \
  --method org.deepin.dde.LocaleHelper1.SetLocale "zh_CN.UTF-8"
```

#### GenerateLocale

生成指定区域设置的 locale 数据。完成后发出 `Success` 信号。

- **输入参数**: `locale`（string, 类型 `s`）：区域名称
- **返回值**: 无

权限：
- requires_sudo: true

```bash
pkexec gdbus call --system \
  --dest org.deepin.dde.LocaleHelper1 \
  --object-path /org/deepin/dde/LocaleHelper1 \
  --method org.deepin.dde.LocaleHelper1.GenerateLocale "zh_CN.UTF-8"
```


### 区域设置信号

#### Success

区域设置生成完成时发出。

- **参数**: `ok`（bool, 类型 `b`）：是否成功；`reason`（string, 类型 `s`）：失败原因（成功时为空）
- **触发条件**: `GenerateLocale` 方法执行完成后发出

```bash
gdbus monitor --system \
  --dest org.deepin.dde.LocaleHelper1 \
  --object-path /org/deepin/dde/LocaleHelper1
```

---
