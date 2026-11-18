# 宿主安装、导入与排错

## 运行条件

- 使用支持 Skills 与本地脚本执行的 UOS AI Agent。技能文件是指令与资源，模型接通 API 本身不会获得本机执行权限。
- 图形登录用户可运行 Python 3.9+ 与 `gdbus`。基础生成/切换用 Python 标准库；实际图标命中验证额外需要系统 GTK3/PyGObject，缺少时报告未验证，不自动装包。
- 脚本与桌面属于同一用户、同一登录会话；不要使用 sudo、SSH 无图形会话或 root 服务代替桌面用户运行。
- 不需要额外启动 MCP 服务；本技能直接调用本机 DDE D-Bus 接口。若环境仅允许 MCP 而不能运行技能脚本，需要另做 MCP 包装，不能声称已完成自动执行。

## 安装与启用

1. 本技能位于 deepin-skills 仓库的 `skills/deepin-theme-guide/`。运行仓库的 `./scripts/install.sh` 安装到 `${SKILL_HOME:-~/.agents}/skills/deepin-theme-guide`；安装 deepin-skills 软件包时位于 `/usr/lib/uos-ai-assistant/skills-default/deepin-theme-guide`。
2. 若 UOS AI 要求通过技能管理入口导入，选择直接包含 `SKILL.md` 的 `deepin-theme-guide/` 目录；需要 ZIP 时打包该目录本身，不要把内容散放到压缩包根目录。
3. 若提示缺少 Agent 环境，按 UOS AI 引导安装应用商店的 **UOS AI Agent**。在部分版本中需要进入 **MCP&Skills** 后启用该技能；版本入口不同，不应假定所有版本菜单一致。
4. 先让 Agent 分别运行 `python3 "<技能目录>/scripts/theme.py" doctor` 和 `python3 "<技能目录>/scripts/theme_pack.py" doctor`。前者检查 DDE 外观接口，后者检查光标编译器和屏保能力。`<技能目录>` 必须是实际安装位置。

官方产品团队对 Agent 安装、Skills/MCP 与版本入口的说明：
[UOS AI 与小U同学问题集中回复](https://bbs.deepin.org.cn/zh/post/300547)。

## 云端模型

首轮可用 Qwen-Plus 的 Function Calling 版本。API Key 保存在 UOS AI 模型配置中，不写入技能、主题请求 JSON 或运行日志。

在百炼控制台复制模型名称和对应地域的 Base URL。对于自动追加 `/chat/completions` 的自定义模型入口，填写截至 `/v1` 的基础地址；地域、业务空间与 API Key 应匹配。模型别名和可用版本以账号控制台为准。

- [统信自定义模型接入说明](https://faq.uniontech.com/tools/ai/6e12)
- [百炼兼容接口配置](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope)
- [百炼工具调用](https://help.aliyun.com/zh/model-studio/qwen-function-calling)

只有在 UOS AI 能把参考图传给视觉模型时，才启用参考图理解。网络壁纸检索使用宿主提供的 Web/图片搜索与浏览工具，下载使用 `wallpaper_source.py`；无搜索工具时应说明能力缺口，可使用用户提供的图片 URL 或本地文件。本包未接入图像生成服务。

本地脚本不上传图片、桌面截图、配置或日志。UOS AI 会把哪些工具结果发送给云端模型由客户端决定；只向模型提供方案所需字段即可，不必发送完整会话环境变量或无关系统信息。

## 首次试用提示词

只读检查：

> 使用 deepin-theme-guide 技能检查我的桌面主题能力，并列出本机可用壁纸、鼠标光标和图标主题。只检查，不修改。请给出不支持的项目和原因。

生成方案：

> 使用 deepin-theme-guide，把桌面搭配成简约深蓝风格。只用本机已有资源，壁纸只改主显示器当前工作区，图标和光标要清晰易辨。先展示实际资源、浅色和深色活动色以及可恢复的变更计划，暂不执行。

自动搜索、下载并应用壁纸：

> 使用 deepin-theme-guide，帮我搜索最适合当前桌面的深蓝星空高清壁纸。我确认由你自动挑选、下载并应用到主显示器当前工作区；按风格和画质选图，不需要逐张询问。完成后告诉我图片来源、验证结果和恢复用的 change ID。

生成新的组件包：

> 使用 deepin-theme-guide 创建一个名为 aurora-blue 的独立主题包：生成统一的基础 SVG 图标和光标源文件，使用我提供的本地壁纸和屏保图片，活动色使用浅色 #406A91、深色 #79A7D2。先生成、校验并预览安装位置，不安装、不激活。

没有准备图片时的试跑：

> 使用 deepin-theme-guide，先检查主题包生成能力，再用技能内置的 assets/aurora-blue.json 在我家目录下创建一个新输出目录，生成并校验基础主题包。展示图标覆盖、光标编译结果和安装预览，暂不安装、不激活。

安装并激活已经展示的包：

> 安装刚才展示的 aurora-blue 主题包，但先不要激活。安装成功后展示光标是否编译、屏保组件是否可用；我确认后再激活图标、光标、活动色、壁纸和图片屏保，并告诉我 change ID。

执行已经展示的方案：

> 应用刚才展示的方案，完成后读回验证，并告诉我用于恢复的 change ID。

恢复：

> 使用 deepin-theme-guide 恢复 change-真实ID 这次修改。如果发现我之后手动改过某项，保留该项并说明。

为已经生效的赛博朋克桌面补齐鼠标：

> 使用技能内置 assets/neon-cyberpunk-cursor.json 创建独立光标包。自动选择可用编译器，生成 24/32/48 三档并验证。先展示用户安装目录，以及 --components cursor --cursor-sync 的激活预览；沿用我对鼠标替换的授权，不修改壁纸、图标或活动色。执行后按主题名验证，并观察配置 20 秒，报告真实 change ID 和未观察的视觉范围。

为已有主题补齐图标：

> 使用新版 deepin-theme-guide，先扫描本机有效应用 Icon 引用，并枚举当前基准图标主题的名称。用 assets/neon-cyberpunk-icons.json 创建新 ID 的独立图标包；该示例采用 base-theme 范围，先确认本机有 bloom，否则用实际基准 ID 替换 base_theme。逐名生成，列出 design-report 中的保留素材、占位图、绝对路径例外和扫描错误。运行 design-preview 查看实际尺寸与明暗背景，icon-audit 检查 GTK/Qt 来源；关键应用可逐个自绘 SVG。若旧包有激活记录，先预览只恢复其 icon 组件，再展示新包 --components icon --launcher-overrides 的安装与激活方案。暂不执行；保留我现有的壁纸、光标、活动色和屏保。

## 故障定位

| 现象 | 排查与处理 |
| --- | --- |
| Agent 只输出命令，没有执行结果 | 检查本地命令工具是否可用；无法执行时可手动运行同一脚本收集 JSON，勿误报成功 |
| `gdbus` 找不到 | 在目标系统确认提供 gdbus 的软件包；本技能不会自动装包 |
| ServiceUnknown | 当前用户会话没有对应外观服务；查 doctor 的新旧接口诊断 |
| Timeout／无法连接 D-Bus | 从桌面用户终端试跑 doctor；确认 Agent 继承用户会话，不要复制其他用户的总线地址 |
| 只有部分能力为 true | 当前版本没有满足读写和回滚要求的接口；保留该项或根据诊断适配，不直接改 GNOME 设置冒充 DDE |
| 缺少 xcursorgen | 自动使用内置标准 ARGB 编译器；仍需 rsvg-convert 光栅化，不必临时编写编译器 |
| 光标 `compiled=false` | 检查 rsvg-convert；缺少光栅化工具时只生成 SVG 源文件，并报告缺项 |
| 主题包安装成功但未切换 | 安装只复制用户资源；需要在用户确认后单独运行 `activate --execute` |
| 只有部分图标变成新风格 | 检查 inventory/coverage 和 icon-audit：是否名称缺失、回退 bloom/hicolor、绝对路径 Icon、应用私有资源或缓存。不要只看 DDE 主题 ID；按 [icons.md](icons.md) 补齐 |
| icon-audit 返回绝对路径例外 | 生成的别名文件还不能接管绝对路径；预览 --launcher-overrides，用户授权后将用户启动器 Icon 键替换并纳入回滚 |
| 图标只有字母而非原应用图形 | 自动匹配失败采用基础徽标；查看 generic_names，为对应名称提供 overrides.source 的原创 SVG |
| 提示激活记录重叠或未完成 | 重叠不再需要回滚：直接激活新包，旧记录归档为 `state=superseded`，仍可按 change ID 恢复。只有 `applying`/`needs_attention` 等未完成记录要先恢复；同一主题包重复激活请恢复旧记录或生成新 ID |
| 包内摘要或安装资源发生变化 | 保留修改的文件；重新根据规范生成新 ID 的包，或先处理现有资源后再试 |
| 屏保图片已安装但未生效 | 激活时必须明确 `--screensaver`，并确认 `dde-dconfig`、`deepin-screensaver` 和自定义屏保组件存在 |
| 壁纸分辨率不足 | 用 `wallpaper_source.py screen` 读取实际分辨率，换一张宽高都 ≥ 屏幕的素材；不要放大。比例差异较大只提示裁切，可继续使用或换更接近的图 |
| 壁纸下载 403/404 或得到网页 | 从来源页找可访问的高清直链，或继续搜索下一张合适候选；不绕过登录或付费访问限制 |
| 壁纸作者或许可未知 | `--author`、`--license` 可省略，来源记录保留未知值；个人桌面使用可沿用用户确认继续下载和应用，不要求版权证明 |
| `execute_ready=false` | 先解决 blocked，或经用户认可后移除不支持的请求项，再重新 plan |
| 计划过期／原值变化 | 重新 inspect 和 plan；不要修改已有计划 JSON 绕过检查 |
| 活动色没变化 | 新接口需要分别设置浅色、深色活动色；检查当前模式与应用是否支持 DDE/DTK 活动色 |
| 光标 DDE 值正确但实际未变 | 运行 cursor_runtime.py 或 theme_pack.py verify，区分配置不一致、按名加载回退、具体应用刷新；同步只通过记录回滚的 --cursor-sync，不临时手改额外配置 |
| applied_pending_runtime | 已写设置但尚未通过运行时验证；保留 change ID，用只读诊断定位，不宣称全部成功 |
| 恢复出现 conflict | 用户或其他程序已改变设置；脚本保留现值。主题包保持 needs_attention，不能卸载；经用户决定将冲突项调回原值后可再次恢复 |

## 后续替换离线模型

保留技能、脚本与 DDE 接口不变，只替换 UOS AI 的模型接入。重新测试工具选择、参数完整性和执行结果判断。模型权重、推理服务和硬件依赖不属于这个主题技能包。
