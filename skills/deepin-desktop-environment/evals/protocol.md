# 可复现评估协议

## 技能发现、触发和参考页读取

`trigger-evals.json` 是触发测试的唯一用例入口。自动化运行器每次遍历完整数组，包括正例、反例和带 `split` 标记的用例；`split` 仅用于分组统计，不作为默认跳过条件。每例只提交 `query` 原文，不附加预期技能、标签或加载指令。`should_trigger` 和 `expected_skill` 仅用于评分。

加载失败、无效 JSON、字段缺失或重复提示词应使测试准备失败，不能静默跳过。结果应记录计划用例数、已运行数及逐例状态；超时和环境错误单列，不能从总数中移除。未运行完全部用例时，报告为未完成。

每例分别记录以下结果，不能以任务成功推导加载成功：

1. **discovered**：新会话实际可用技能列表含 `deepin-desktop-environment`，记录解析后的描述、实际路径、版本/hash 和加载错误。仓库 `skills/` 或 ZIP 文件存在不代表已经安装。若没有发现，先修复测试环境，不能统计为描述未触发。聚合技能与旧组件技能并存时保留候选列表；只读取旧组件技能不算读取了本技能。
2. **skill_loaded / references_read**：保存工具调用及读取响应，确认 agent 自主读取入口和任务所需参考页。提到技能名、列出路径、从父会话继承内容或预加载正文均不算自主读取；读取相关章节即可，不要求载入整套文档。
3. **task_passed**：对照本次实际接口响应核验答案、语义与操作边界。接口缺失可以是正确的探测结论；环境错误不得伪装为 false、零或空集合。保留任务通过但技能未读取的结果。

安装修订版后重新发现技能或启动新会话。技能应安装到所用 Agent 配置的技能目录，并确认该环境能够发现入口 `deepin-desktop-environment/SKILL.md`。不要为测试关闭其他候选技能或显式指定本技能。分别测试修改前后的描述，使用相同候选列表、模型、权限和系统状态，建议每条运行三次；`split: validation` 的提示词单独统计，不能将规则匹配或人工接口重放称为模型触发率。

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

## 执行环境与结果口径

触发测试逐例使用独立会话，保留其他候选技能可见；默认覆盖整个触发集。涉及启动应用、发送通知或修改配置的提示词在隔离测试桌面执行。仅探测方法签名不代表实际操作完成。

接口查询使用本次返回值。布局候选集合与已添加集合、DConfig 配置项与 X 设置属性分别记录语义；服务缺失、权限错误与空集合、零、false 分开。未指定接口的任务允许语义等价的实现路径，技能触发结果和任务完成结果分别评分。

写入测试由夹具记录原值，结束或异常后恢复并回读，分别保留任务和清理证据。多组件任务只将本技能提供的能力纳入其接口断言。

`workflow-evals.json` 单独验证执行行为、授权边界和恢复流程，使用 `prompt`、断言与模拟状态，不作为另一份触发用例入口。`scripts/evaluate-trace.py` 只检查已有动作记录，不负责运行模型或评估自主触发。
