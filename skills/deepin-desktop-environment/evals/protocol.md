# 可复现评估协议

## 固定输入

三个可执行场景使用 [模拟状态](../assets/evals/fixtures.json)：`appearance`、`power`、`readback-failure`，对应 workflow-evals 中的 1、2、10。图片使用 [固定壁纸](../assets/evals/wallpaper.svg)。输入包含用户、会话、服务、原值、权限、单位、目标值和写入响应；失败场景明确规定写入返回成功但状态不改变。

这三个场景禁止访问真实桌面总线。由评估者或评估运行器按 fixture 提供工具响应；允许 Agent 按需读取 Skill 内资料。其余工作流场景仍用于人工检查边界，不计入这三个场景的通过率。

## with-skill 与 baseline

1. 在两个独立、无会话历史的隔离会话中使用相同模型、工具权限、prompt 和 fixture 响应。一组提供本 Skill，另一组不提供；均不预先提供 expected_value、required_writes 和 expected_success 等评分答案。
2. 工具读取使用 fixture 的 probe、metadata 和 initial_value；写入按 fixture 更新模拟状态。ignore_writes 为 true 时返回 write_response 但不更新值；后续读取保持原值。图片绝对路径由运行器展开，原始工具记录保留该路径。
3. 保存两组原始工具调用、回复和归一化动作，以及运行时间、模型与 token 数。归一化只转换表示方式，不能补充模型没有执行的探测、读取、回滚记录或回读。
4. 用下述脚本检查两组动作；人工核对最终回复、真实命令参数与动作归一化是否一致，再给出通过率、时间、token 的差值。未运行模型时不得用人工参考动作充当模型或 baseline 成绩。

## 动作格式与检查

将动作保存为 JSON 数组。`probe` 返回环境信息；`metadata` 返回目标项元数据；`read` 返回模拟当前值；`write` 按 fixture 修改；最后 `report` 记录是否成功及恢复所需原值。

```json
[
  {"op": "probe"},
  {"op": "metadata", "key": "sidebarWidth", "bus": "system", "api": "dde-dconfig", "config_appid": "org.deepin.dde.control-center", "config_resource": "org.deepin.dde.control-center"},
  {"op": "read", "key": "sidebarWidth", "bus": "system", "api": "dde-dconfig", "config_appid": "org.deepin.dde.control-center", "config_resource": "org.deepin.dde.control-center"},
  {"op": "write", "key": "sidebarWidth", "bus": "system", "api": "dde-dconfig", "config_appid": "org.deepin.dde.control-center", "config_resource": "org.deepin.dde.control-center", "value": 200},
  {"op": "read", "key": "sidebarWidth", "bus": "system", "api": "dde-dconfig", "config_appid": "org.deepin.dde.control-center", "config_resource": "org.deepin.dde.control-center"},
  {"op": "report", "success": false, "original_values": {"sidebarWidth": 180}}
]
```

D-Bus 动作的 bus、read_api、write_api 来自 fixture；实际服务、对象路径、完整参数和类型仍需对照原始工具记录人工核验。workspace_1 的图片 URI 归一化为 `assets/evals/wallpaper.svg`。DConfig 动作保留 appId 和 resource，不能将 Session 电源接口与 System 总线上的 DConfig 管理服务混为一谈。

在 Skill 根目录运行：

```bash
python3 scripts/evaluate-trace.py readback-failure /tmp/actions.json
```

脚本仅在内存中重放动作并输出检查证据，不调用系统命令、不连接 D-Bus、不修改真实配置。它检查目标、单位、总线、资源、未授权额外写入、回读、恢复原值记录和最终状态报告；命令行细节及回复质量仍由人工检查。退出码 0 表示动作检查通过，1 表示失败。

## 桌面状态与接口集成用例

`desktop-state-evals.json` 是本 skill 的常驻测试集，覆盖当前外观、会话 PID、认证代理、键盘布局、XSettings、快捷键类别、注册应用和跨组件汇总。用例 ID 独立编号，不依赖外部报告。原始提示词和断言均在用例文件中维护。

将 skill 安装到测试会话可发现的技能目录，保持其他候选技能可见；每例启动独立会话，只输入 prompt 原文，不使用 `$deepin-desktop-environment` 或额外加载指令。在已运行相关服务的测试会话中逐例执行，不为满足只读用例启动应用。应用名称用例需要注册 deepin-editor；最近文件用例需要已运行的文件管理器服务。环境不满足时记录具体前置缺失，不将空值或零当作成功结果。写入用例只允许双击间隔目标键，测试夹具在执行前记录原值，并在结束或异常后恢复、回读；分别保存任务和清理阶段证据。

动态值以本次调用结果为准。快捷键类别分别覆盖具备类别枚举接口和缺失该接口的部署；若后者使用模拟响应，单独标注模拟结果。每次变更保留失败证据，修复后重测受影响用例，注明沿用和新执行的结果。每例同时检查自动触发与任务结果：工具记录须证明 agent 自行读取本 skill 的 SKILL.md，仅在回复中提及技能名不算触发；未触发即该断言失败。13 条原始提示词也收录到 `trigger-evals.json`，参与既有正反例触发评测；两个文件中提示词须保持一致。触发评测每例独立运行，建议重复三次并分别记录加载次数、执行成功次数、超时和环境错误。原先显式加载的执行成绩不能作为自动触发通过证据。
