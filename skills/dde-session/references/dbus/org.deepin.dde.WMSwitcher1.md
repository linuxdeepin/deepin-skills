# org.deepin.dde.WMSwitcher1 接口参考

该接口提供窗口管理器查询和切换能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.WMSwitcher1` |
| Object path | `/org/deepin/dde/WMSwitcher1` |
| Interface | `org.deepin.dde.WMSwitcher1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 窗口管理器操作

#### AllowSwitch

查询是否允许切换窗口管理器。

- **输入参数**: 无
- **返回值**: `b`（bool）：是否允许

```bash
gdbus call --session \
  --dest org.deepin.dde.WMSwitcher1 \
  --object-path /org/deepin/dde/WMSwitcher1 \
  --method org.deepin.dde.WMSwitcher1.AllowSwitch
```

#### CurrentWM

获取当前窗口管理器名称。

- **输入参数**: 无
- **返回值**: `s`（string）：当前窗口管理器名称

```bash
gdbus call --session \
  --dest org.deepin.dde.WMSwitcher1 \
  --object-path /org/deepin/dde/WMSwitcher1 \
  --method org.deepin.dde.WMSwitcher1.CurrentWM
```

#### RequestSwitchWM

请求切换窗口管理器。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.WMSwitcher1 \
  --object-path /org/deepin/dde/WMSwitcher1 \
  --method org.deepin.dde.WMSwitcher1.RequestSwitchWM
```


### 窗口管理器信号

#### WMChanged

窗口管理器切换时发出。

- **参数**: `wmName`（string, 类型 `s`）：新窗口管理器名称
- **触发条件**: 窗口管理器切换时发出

```bash
gdbus monitor --session \
  --dest org.deepin.dde.WMSwitcher1 \
  --object-path /org/deepin/dde/WMSwitcher1
```

