# org.deepin.dde.dialog1 接口参考

该接口提供系统级对话框的显示、取消和代理响应能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.dialog1` |
| Object path | `/org/deepin/dde/dialog1` |
| Interface | `org.deepin.dde.dialog1` |
| Bus | System |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。


### 对话框操作

#### Open

打开系统对话框。

> **待核验**: `type` 参数支持固定的对话框类型选项，具体选项值待核验源码确认。

- **输入参数**: `type`（string, 类型 `s`）：对话框类型；`title`（string, 类型 `s`）：标题；`message`（string, 类型 `s`）：消息内容；`icon`（string, 类型 `s`）：图标；`button_name`（string, 类型 `s`）：按钮名称
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.dialog1 \
  --object-path /org/deepin/dde/dialog1 \
  --method org.deepin.dde.dialog1.Open "confirm" "标题" "消息内容" "dialog-information" "确定"
```

#### Cancel

取消指定类型的对话框。

> **待核验**: `type` 参数支持固定的对话框类型选项，具体选项值待核验源码确认。

- **输入参数**: `type`（string, 类型 `s`）：对话框类型
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.dialog1 \
  --object-path /org/deepin/dde/dialog1 \
  --method org.deepin.dde.dialog1.Cancel "confirm"
```


### 代理管理

#### RegisterAgent

注册对话框代理。

- **输入参数**: `service`（string, 类型 `s`）：代理服务名；`path`（string, 类型 `s`）：代理对象路径
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.dialog1 \
  --object-path /org/deepin/dde/dialog1 \
  --method org.deepin.dde.dialog1.RegisterAgent "com.example.Agent" "/com/example/Agent"
```

#### UnregisterAgent

注销对话框代理。

- **输入参数**: `service`（string, 类型 `s`）：代理服务名；`path`（string, 类型 `s`）：代理对象路径
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.dialog1 \
  --object-path /org/deepin/dde/dialog1 \
  --method org.deepin.dde.dialog1.UnregisterAgent "com.example.Agent" "/com/example/Agent"
```

#### AgentResponse

代理响应对话框。

> **待核验**: `type` 参数支持固定的对话框类型选项，具体选项值待核验源码确认。

- **输入参数**: `type`（string, 类型 `s`）：对话框类型；`button_index`（int32, 类型 `i`）：按钮索引
- **返回值**: 无

```bash
gdbus call --system \
  --dest org.deepin.dde.dialog1 \
  --object-path /org/deepin/dde/dialog1 \
  --method org.deepin.dde.dialog1.AgentResponse "confirm" 0
```

---
