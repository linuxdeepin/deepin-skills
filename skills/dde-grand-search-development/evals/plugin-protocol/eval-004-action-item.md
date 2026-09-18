# Eval: 实现 Action 接口

## 任务

用户点击插件返回的搜索结果后，插件需要打开对应的文件或启动对应的应用。请实现 `Action` 接口。

## 期望输出

回答应：
1. 解析输入 JSON，取出 `ver`、`action`、`item` 三个字段
2. 校验 `ver` 为 `"1.0"`，校验 `action` 为 `"openitem"`
3. 根据 `item` 定位结果并执行操作（打开文件、启动应用、复制内容等）
4. 返回 `true`/`false` 表示成功与失败
5. 说明 `item` 应设计为自描述格式，因为 Action 走独立的临时连接
6. 说明 daemon 不处理返回值，但仍应正确返回便于排查

## 验证要点

- [ ] 从 JSON 中正确取出 `action` 与 `item`（字段名为 `action`/`item`）
- [ ] 判断 `action == "openitem"`
- [ ] 根据 `item` 定位并执行操作，而不是忽略 `item`
- [ ] 返回布尔值
- [ ] 指出 Action 连接独立，`item` 需自描述或需缓存加锁
- [ ] JSON 解析失败时返回 `false` 并记录日志

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 正确解析并路由 `openitem`，`item` 可定位结果，返回值与错误处理完整 |
| ⚠️ **PARTIAL** | 接口实现正确但未说明 Action 连接独立带来的定位风险 |
| ❌ **FAIL** | 忽略 `item` 字段，或未区分 `action` 类型 |

## 反模式检查

- [ ] 未假设 daemon 会传 `openitem` 之外的其他 action 值
- [ ] 未声称 daemon 会依据返回值提示用户
- [ ] 未在 `Action` 中依赖搜索期间的易失内存状态而不加锁
