# org.deepin.dde.ControlCenter1.GrandSearch 接口参考

该接口在 Session 总线上注册，对象路径为 `/org/deepin/dde/ControlCenter1`，提供控制中心内全局搜索能力，支持搜索、停止搜索和执行搜索动作。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.ControlCenter1` |
| Object path | `/org/deepin/dde/ControlCenter1` |
| Interface | `org.deepin.dde.ControlCenter1.GrandSearch` |
| Bus | Session |

### 全局搜索操作

#### Search

执行全局搜索。

- **功能**: 根据用户输入的搜索关键词，在控制中心所有设置模块中搜索匹配项，返回搜索结果 JSON。
- **触发条件**: 当用户在控制中心搜索框输入关键词时调用。
- **使用场景**: 用户在控制中心搜索框中输入"亮度"、"蓝牙"关键词时，dde-shell 搜索服务调用此方法获取控制中心内的匹配设置项。
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

- **功能**: 停止当前正在进行的全局搜索，清理搜索状态。
- **触发条件**: 当用户清除搜索框内容或关闭搜索面板时调用。
- **使用场景**: 用户清空搜索框或切换离开搜索面板时，dde-shell 搜索服务调用此方法通知控制中心停止搜索。
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

- **功能**: 根据用户选择的搜索结果项，执行对应的动作（跳转到对应设置页面）。
- **触发条件**: 当用户点击搜索结果中的某一项时调用。
- **使用场景**: 用户在搜索结果中点击"屏幕亮度"项后，dde-shell 搜索服务调用此方法通知控制中心跳转到显示设置页面。
- **输入参数**: `json`（string, 类型 `s`）：动作请求 JSON
- **返回值**: `b`（bool）：是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.ControlCenter1 \
  --object-path /org/deepin/dde/ControlCenter1 \
  --method org.deepin.dde.ControlCenter1.GrandSearch.Action '{"action":"open","item":"display"}'
```
