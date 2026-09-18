# Eval: 构造合法的搜索结果 JSON

## 任务

插件搜索到了两条结果（一条是 PDF 文件 `/home/user/report.pdf`，一条是应用 `org.example.Notes`），分组名为「我的笔记」。请给出 `Search` 接口应返回的完整 JSON。

## 期望输出

回答应：
1. 返回 `ver` 为 `"1.0"`、`mID` 与输入一致、`cont` 为数组
2. `cont[].group` 填「我的笔记」
3. 每个结果项包含 `item`/`name`/`type`，`icon` 可选
4. PDF 文件的 `type` 填 `application/pdf`（真实 MIME type）
5. 应用的 `type` 填语义化自定义值（如 `application/x-desktop-app`），不要留空
6. `item` 为组内唯一的标识，且能在 `Action` 时定位到结果

## 验证要点

- [ ] 结果 `ver` 为 `"1.0"`
- [ ] `mID` 与输入保持一致
- [ ] `cont` 是数组，且 `group` 非空
- [ ] 每个 item 的 `item`/`name`/`type` 均非空
- [ ] PDF 的 `type` 为 `application/pdf`（或等价有效 MIME type）
- [ ] 应用项的 `type` 为语义化自定义值而非空字符串
- [ ] `item` 具备唯一性且可自描述（如包含路径或应用 ID）
- [ ] 未在结果项中加入 `itemLevel`/`itemTailer` 等扩展属性

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | JSON 结构完整合法，必填字段齐全，`type` 取值合理且 `item` 可定位 |
| ⚠️ **PARTIAL** | 结构正确但 `type` 全部填同一自定义值，或 `item` 只是序号无定位信息 |
| ❌ **FAIL** | `ver` 缺失或非 `1.0`，或 item 中缺少 `item`/`name`/`type` 任一字段 |

## 反模式检查

- [ ] 未省略 `ver` 或填写非 `1.0` 的值
- [ ] 未在结果项中使用 `itemLevel`/`itemTailer`/`itemWeight` 等扩展属性
- [ ] 未把 `type` 留空
- [ ] 未在 `name` 中放置未本地化的硬编码英文分组名（分组名需按系统语言返回）
