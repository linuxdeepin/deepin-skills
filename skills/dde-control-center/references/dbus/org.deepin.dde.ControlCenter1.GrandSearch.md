# org.deepin.dde.ControlCenter1.GrandSearch 接口参考

该接口提供控制中心内全局搜索能力，支持搜索、停止搜索和执行搜索动作。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ControlCenter1` |
| Object path | `/org/deepin/dde/ControlCenter1` |
| Interface | `org.deepin.dde.ControlCenter1.GrandSearch` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 全局搜索操作

#### Search

执行全局搜索。

- **输入参数**: `json`（string, 类型 `s`）：搜索请求 JSON
- **返回值**: `s`（string）：搜索结果 JSON

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.GrandSearch.Search '{"search":"brightness"}'
```

#### Stop

停止搜索。

- **输入参数**: `json`（string, 类型 `s`）：停止请求 JSON
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.GrandSearch.Stop '{"search":"brightness"}'
```

#### Action

执行搜索结果动作。

- **输入参数**: `json`（string, 类型 `s`）：动作请求 JSON
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.GrandSearch.Action '{"action":"open","item":"display"}'
```

---
