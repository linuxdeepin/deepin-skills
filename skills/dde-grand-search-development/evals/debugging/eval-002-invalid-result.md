# Eval: 插件已加载但搜索无结果

## 任务

daemon 日志里有 `Added plugin` 和 `Starting program`，插件进程也在运行，但搜索时界面里没有结果。daemon 日志中有 `Invalid result format from plugin`。请分析原因。

## 期望输出

回答应：
1. 指出该日志来自 `ConvertorV1_0::result` 解析失败，原因是结果 JSON 不符合 V1.0 规范
2. 首先怀疑结果 JSON 的 `ver` 未回填或不是 `"1.0"`（这是最常见成因）
3. 检查 `mID` 是否为空或未与输入一致
4. 检查 `cont` 是否为数组
5. 建议用 `dbus-send` 直接调用插件的 `Search` 接口，把返回的 JSON 单独取出来核对
6. 提醒结果项 `item`/`name`/`type` 为空会被跳过（但不会产生这条日志，属于另一种「部分结果丢失」）

## 验证要点

- [ ] 正确解读 `Invalid result format from plugin` 的含义
- [ ] 首要怀疑 `ver` 未回填或不为 `1.0`
- [ ] 检查 `mID` 与 `cont` 的类型
- [ ] 建议用 `dbus-send` 绕开 daemon 单独验证接口
- [ ] 区分「整个结果集被丢弃」与「部分结果项被跳过」两类问题

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 准确定位到结果 JSON 格式问题，优先指出 `ver` 校验，并给出 dbus-send 隔离验证方法 |
| ⚠️ **PARTIAL** | 定位到 JSON 格式问题但未指出 `ver` 这一首要成因，或未给出隔离验证方法 |
| ❌ **FAIL** | 归因于 daemon 或界面 bug，或建议修改 daemon 的解析逻辑 |

## 反模式检查

- [ ] 未建议修改 daemon 的 `ConvertorV1_0`
- [ ] 未忽略日志线索去排查 conf 或进程启动
- [ ] 未把 `ver` 问题与 `InterfaceVersion` 混淆（两者都必须是 `1.0`，但校验位置不同）
