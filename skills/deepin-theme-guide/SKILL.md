---
name: deepin-theme-guide
description: 用于 deepin/UOS DDE 全局主题的完整开发：既指导选用已有应用样式、图标、字体和光标并编写 index.theme、亮暗配置、预览与目录，也提供自带脚本生成、安装、激活、验证和恢复主题资源包，覆盖图标与光标制作、壁纸搜索下载、图片屏保、活动色、控制中心注册和 GTK 适配。当用户要求做一套主题、编写或排查 index.theme、从零生成图标或光标、替换壁纸、安装并切换主题，或恢复主题变更时使用。单次查询或切换现有外观设置使用 deepin-desktop-environment；DTK 应用内的主题跟随实现使用 dtk-development。
---

# deepin 主题开发指南

本 Skill 覆盖两条工作流，共用同一套主题格式、目录位置和 DDE 外观接口知识。先判断用户只需要组合已有资源，还是需要生成、安装和恢复资源，再读取对应流程。

## 能力边界

- **组合编写**：选用已有应用样式、图标主题、字体和光标主题，编写完整 `index.theme`，组织亮暗配置、预览、壁纸和 GTK 适配。
- **生成托管**：用自带脚本生成图标、光标、壁纸、图片屏保和局部主题卡片，安装、激活、验证并恢复。
- 只查询或单次切换一个现有外观项（字体、图标、光标、壁纸、活动色）时使用 `$deepin-desktop-environment`；需要多组件组合、预览或恢复的现有资源切换可使用本 Skill 的生成托管工作流。
- 两条路径不能混用：生成器安装的目录带 manifest 和安装清单，手工改动会在激活、验证或卸载时被拒绝。

## 选择工作流

| 用户意图 | 工作流 | 首先读取 |
| --- | --- | --- |
| 组合已有资源、编写或排查 `index.theme`、亮暗配置、GTK 适配 | 组合编写 | [global-theme.md](references/global-theme.md)、[resources.md](references/resources.md) |
| 从零生成图标、光标、壁纸或屏保；对现有资源做带预览/恢复的多组件切换；安装、激活、恢复主题包 | 生成托管 | [package-workflow.md](references/package-workflow.md) |
| 完整主题，同时需要生成图标或光标 | 混合流程 | 本页“混合流程”、[global-theme.md](references/global-theme.md)、[package-workflow.md](references/package-workflow.md) |
| 只做单次现有外观查询或切换 | 不在本 Skill | 使用 `$deepin-desktop-environment` |

## 工作流 A：组合编写

1. **确定主题身份与范围。** 使用独立主题 ID，确定显示名称、亮暗模式以及用户指定的配色、壁纸和资源偏好。默认编写亮暗两个配置分组。
2. **选择已有资源。** 读取 [资源选择](references/resources.md)，确定应用样式、图标、光标、标准字体和等宽字体。需要查询时使用 `$deepin-desktop-environment` 的 Appearance1 服务。
3. **编写主题配置。** 读取 [配置与存放规则](references/global-theme.md)，以 [index.theme 模板](assets/index.theme) 为起点，填写所选资源、字号、亮暗活动色和壁纸引用。模板名称是示例，必须替换为实际可用值。
4. **组织主题目录。** 准备工作目录中的 `index.theme`、预览和需要随主题提供的壁纸；复用已安装资源时保留有效引用并列出依赖。用户要求安装时，部署到用户或系统主题目录。
5. **交付完整组合。** 给出目录、资源选择清单、安装位置及 `主题ID.light` / `主题ID.dark` 选择值；确认每项引用都有资源或明确依赖。实际选择主题使用 `$deepin-desktop-environment` 的 Appearance1 服务。

关键约束：

- 全局主题 ID 与 `AppTheme`、`IconTheme`、`CursorTheme` 的资源名相互独立，不要用显示名称代替。
- 默认分组写完整组合，暗色分组只写差异项；空值继承默认分组，无效资源名不构成继承。
- 字体用 `StandardFont`、`MonospaceFont`、`FontSize` 表达，没有 `FontTheme` 字段。
- `ActiveColor` 不会自动改写 GTK CSS；需要统一配色时读取 [GTK 主题适配](references/gtk-adaptation.md)。
- 手工部署的主题由用户或 Appearance1 选择；不要让生成器接管手工目录。

主题生效机制、XSettings 映射和刷新条件见 [theme-mechanism.md](references/theme-mechanism.md)。

## 工作流 B：生成托管

先完整读取 [package-workflow.md](references/package-workflow.md)，再按任务读取图标、光标、壁纸、屏保和恢复文档。核心约束：

- 从实际加载的 `SKILL.md` 路径确定 `<技能目录>`，先运行 `theme.py doctor` 和 `theme_pack.py doctor`；缺少依赖时如实报告，不自动安装。
- 只使用自带脚本和固定命令，不手写 `gsettings`/`xrdb`、不覆盖系统目录、不用 sudo 绕过。系统写入只在用户授权范围覆盖时加 `--execute`。
- 生成前先确定造型、材质和辨识特征；图标默认 `design_policy=restyle-apps`，逐应用重绘用 `custom-apps`。`create/validate` 成功只表示包完整，`design_complete`、`scope_complete` 和实际视觉质量分别报告。
- 安装与激活分开。`install --execute` 注册控制中心卡片、安装图标/光标目录、导入自定义壁纸并保存恢复记录；`installed=true,ok=false` 表示文件已装好但可见性未验证。
- 激活后报告真实 `change-<ID>`。`applied_pending_runtime`、`scope_complete=false`、`needs_attention` 必须如实报告；视觉状态默认未观察。
- 生成包、安装记录和状态目录沿用 `uos-theme-personalize` 标识，以兼容既有包和恢复记录；它们现在由本 Skill 管理。
- 只切换现有资源时，用 `theme.py plan --request` 生成可审阅计划，再 `apply --execute`；单次外观项仍优先使用 `$deepin-desktop-environment`。
- 图标全量覆盖、设计完成度与绝对路径例外见 [icons.md](references/icons.md)、[design.md](references/design.md)；控制中心注册和原生切换见 [control-center.md](references/control-center.md)；状态与验收语义见 [scripts.md](references/scripts.md)。

## 混合流程：完整主题 + 生成资源

生成器写出的主题卡片只包含实际请求的 `IconTheme`、`CursorTheme`、`Wallpaper` 和 `ActiveColor`，不会补 `AppTheme`、字体、锁屏或窗口参数。需要完整主题时：

1. 按工作流 A 编写完整 `index.theme`，图标和光标字段指向计划生成的 ID。
2. 按工作流 B 生成并安装图标/光标资源。若不想让生成器写入局部卡片，使用 `install --no-desktop-integration`；该模式不注册控制中心卡片、不导入壁纸，但仍把图标/光标安装到用户资源目录。
3. 用 `activate --components icon,cursor` 应用资源，或按工作流 A 手工部署完整主题后由 `$deepin-desktop-environment` 选择。
4. 不要把生成器安装的卡片当作完整主题再手动补字段：激活、验证或卸载会因安装清单变化拒绝继续。需要改字段时重新生成，或采用本流程的手工卡片。

## 通用交付约束

- 区分文件生成、配置读回、配置层一致、按名加载和实际视觉观察；缺少视觉工具时明确未观察。
- 保留已有授权，不要求用户重复确认同一范围；新增范围单独说明。
- 失败、冲突和未完成状态按脚本报告，不把命令提交当作已经生效。
- 交付时给出主题 ID、安装位置、所选资源或生成组件、验证结果和恢复用 change ID。

## 参考资料

### 组合编写

| 场景 | 文档 |
| --- | --- |
| 主题身份、`index.theme` 字段、亮暗继承与存放目录 | [global-theme.md](references/global-theme.md) |
| 已有应用样式、图标、字体、光标的查询与选择 | [resources.md](references/resources.md) |
| 设置发布、Qt/GTK 使用方式、刷新与工具包范围 | [theme-mechanism.md](references/theme-mechanism.md) |
| GTK 亮暗子主题、配色覆盖与接入 | [gtk-adaptation.md](references/gtk-adaptation.md) |

### 生成托管

| 场景 | 文档 |
| --- | --- |
| 完整命令行流程、授权、状态和恢复边界 | [package-workflow.md](references/package-workflow.md) |
| 主题包格式、设计规范、生成组件与安装边界 | [package.md](references/package.md) |
| 图标造型、代表稿、实际尺寸预览与自定义素材 | [design.md](references/design.md) |
| 图标扫描、全量覆盖、设计完成度与绝对路径例外 | [icons.md](references/icons.md) |
| 光标编译、多层验证、配置同步与旧变更边界 | [cursor.md](references/cursor.md) |
| 壁纸搜索、分辨率检测、下载应用与来源记录 | [wallpaper.md](references/wallpaper.md) |
| 控制中心注册、原生鼠标切换与安装清理 | [control-center.md](references/control-center.md) |
| CLI 输出、状态文件、恢复语义与验收方法 | [scripts.md](references/scripts.md) |
| 已有资源切换的请求字段与搭配规则 | [requests.md](references/requests.md) |
| 图标、光标和图片屏保的格式限制 | [assets.md](references/assets.md) |
| DDE 新旧接口、活动色差异、兼容性与官方来源 | [dde-api.md](references/dde-api.md) |
| 宿主安装、导入、模型配置与排错 | [host-setup.md](references/host-setup.md) |
