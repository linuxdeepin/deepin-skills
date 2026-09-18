# Eval: 说明 Action 的触发链路与结果定位策略

## 任务

用户问：「我的插件返回了搜索结果，用户点击结果后我的插件要怎么知道点的是哪一项？我在 Search 时把结果存在了 QHash 里，Action 时去查这个 QHash，可以吗？」

请说明 Action 的触发链路，并评估这种实现方式。

## 期望输出

回答应：
1. 说明链路：前端 → daemon `OpenWithPlugin(searcher, item)` → `searcherAction(searcher, "openitem", item)` → 插件 `Action(json)`
2. 说明 `searcher` 是插件的 `Name`（conf 中的值），`item` 是结果项中的 `item` 字段
3. 指出 `Action` 由 daemon 新建的临时连接发起，与搜索时的实例不同，进程可能已退出
4. 评估 QHash 缓存方案的风险，并给出更稳妥的自描述 `item` 方案（如 `file:/path`、`app:org.example.App`）
5. 说明 daemon 只会传 `action="openitem"`
6. 说明 daemon 不处理 `Action` 的返回值，但插件仍应返回 `true`/`false`

## 验证要点

- [ ] 完整描述了前端 → daemon → 插件的 Action 链路
- [ ] 正确说明 `searcher` 即插件 `Name`，`item` 即结果项 `item`
- [ ] 指出 Action 使用独立的临时连接，不共享搜索时的实例状态
- [ ] 给出了自描述 `item` 的改进方案，或至少指出缓存方案的进程生命周期风险
- [ ] 说明 `action` 当前仅 `openitem`
- [ ] 未声称 daemon 会依据返回值做重试或提示

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 链路描述完整，并指出缓存方案的进程生命周期风险且给出自描述 item 方案 |
| ⚠️ **PARTIAL** | 链路描述正确，但未指出 Action 连接独立带来的状态风险 |
| ❌ **FAIL** | 错误描述 Action 链路，或断言缓存方案一定安全 |

## 反模式检查

- [ ] 未声称 daemon 会传 `openitem` 之外的其他 action 值
- [ ] 未声称 daemon 会依据 Action 返回值做用户提示或重试
- [ ] 未把 `item` 描述为界面展示字段
