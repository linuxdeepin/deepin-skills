# dde-grand-search-development Evals

本目录包含 DDE 全局搜索扩展搜索插件开发的验证测试用例，按 references 文档结构分类。

## 目录结构

```
evals/
├── architecture/          # 架构与接入形态 evals
├── plugin-protocol/       # V1.0 接口与数据格式 evals
├── plugin-config/         # 插件配置与运行模式 evals
├── plugin-development/    # 工程、构建、打包、国际化 evals
├── debugging/             # 故障排查 evals
├── cross-skill/           # 跨 skill 依赖 evals
├── trigger-evals.json     # 触发评估（全部）
├── trigger-evals-train.json
├── trigger-evals-validation.json
└── eval-template.md       # 模板文件
```

## 评分标准

每个 eval 包含四段结构：

| 节 | 说明 |
|----|------|
| 任务 | 具体的开发任务描述 |
| 期望输出 | 代码或回答应具备的特征 |
| 验证要点 | 检查清单 |
| 评分标准 | PASS / PARTIAL / FAIL 三级评分 + 反模式检查 |

## Evals 列表

### architecture (3 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | plugin-form | 识别插件是 `.conf` + DBus 服务，而非 `.so` 插件 |
| eval-002 | result-limits | 结果解析上限与必填字段限制 |
| eval-003 | action-flow | Action 触发链路与结果定位策略 |

### plugin-protocol (5 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | dbus-interface | 实现 V1.0 三个 DBus 接口与会话总线注册 |
| eval-002 | result-json | 构造合法的搜索结果 JSON |
| eval-003 | interruptible-search | 实现可被 Stop 中断的 Search |
| eval-004 | action-item | 实现 Action 接口与结果定位 |
| eval-005 | type-preview | `type` 字段与预览插件匹配 |

### plugin-config (4 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | conf-basic | 编写插件配置文件 |
| eval-002 | run-mode | 运行模式与优先级选择 |
| eval-003 | trigger-mode | Trigger 模式与 D-Bus service 文件 |
| eval-004 | name-conflict | 内置搜索项冲突与命名规范 |

### plugin-development (4 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | project-setup | 从零创建插件工程 |
| eval-002 | cmake-install | CMake 安装规则与 conf 生成 |
| eval-003 | debian-packaging | Debian 打包 |
| eval-004 | i18n | 分组名与结果名的国际化 |

### debugging (4 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | plugin-not-loaded | 插件未被加载的排查 |
| eval-002 | invalid-result | 结果 JSON 格式错误导致无结果 |
| eval-003 | dbus-send | 用 dbus-send 隔离验证接口 |
| eval-004 | timeout-interrupt | 搜索超时与中断失效排查 |

### cross-skill (1 个)

| 编号 | 文件 | 测试点 |
|------|------|--------|
| eval-001 | dtk-host-app | 为已常驻的 DTK 应用接入全局搜索（Manual 模式），并按需加载 `$dtk-development` |

## 触发评估

`trigger-evals.json` 包含 30 条触发测试（18 正例 + 12 反例），其中 1 条为跨 skill 测试（同时涉及 DConfig 与 DIconTheme，验证 `$dtk-development` 交叉触发）。`trigger-evals-train.json`（17 条）与 `trigger-evals-validation.json`（13 条）是全集的划分，两者不重叠且并集等于全集。

反例覆盖了容易与全局搜索插件混淆的场景：托盘插件、Shell 插件、控制中心插件、DTK 通用开发，以及「只是使用全局搜索」而非开发插件的普通提问。

## 运行

`scripts/run-eval.sh` 可用来自动化执行单个 output-quality eval（对比启用 skill 与基线）：

```bash
scripts/run-eval.sh --eval evals/plugin-protocol/eval-001-dbus-interface.md -- \
  <AGENT_COMMAND>
```

## 总计

共 **22** 个 output-quality evals（含 eval-template.md），覆盖全局搜索扩展搜索插件开发的核心场景。
