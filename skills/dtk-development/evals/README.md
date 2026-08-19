# DTK Skill Evals

本目录包含用于验证 dtk-development skill 有效性的测试用例。

## 目录结构

Evals 按 skill 的 references 目录分类组织：

```
evals/
├── widgets/           # QWidget 控件测试 (W-001 ~ W-030)
├── declarative/       # 仅 v25 DTK QML 控件测试 (Q-001 ~ Q-012)
├── theme/             # 主题系统测试 (T-001 ~ T-008)
├── config/            # DConfig 配置测试 (C-001 ~ C-006)
├── utilities/         # 工具类测试 (U-001 ~ U-006)
├── debugging/         # 调试场景测试 (D-001 ~ D-005)
├── custom-controls/   # 自定义控件测试 (X-001 ~ X-006)
├── project-setup/     # 工程配置测试 (P-001)
├── architecture/      # 架构理解测试 (A-001 ~ A-004)
└── platform/          # 平台抽象测试 (L-001 ~ L-003)
```

## Evals 列表

### widgets/ - QWidget 控件

| 编号 | 测试场景 | 文件 |
|------|----------|------|
| W-001 | 创建带警告样式的对话框 | [widgets/eval-001-dialog-warning.md](widgets/eval-001-dialog-warning.md) |
| W-002 | DIconButton 使用 dci 图标 | [widgets/eval-002-iconbutton-dci.md](widgets/eval-002-iconbutton-dci.md) |
| W-003 | 主窗口与标题栏 | [widgets/eval-003-mainwindow-titlebar.md](widgets/eval-003-mainwindow-titlebar.md) |
| W-004 | 输入框验证 | [widgets/eval-004-input-validation.md](widgets/eval-004-input-validation.md) |
| W-005 | 按钮类型选择 | [widgets/eval-005-button-types.md](widgets/eval-005-button-types.md) |
| W-006 | 开关按钮 | [widgets/eval-006-switch-button.md](widgets/eval-006-switch-button.md) |
| W-007 | 按钮组 | [widgets/eval-007-button-box.md](widgets/eval-007-button-box.md) |
| W-008 | 浮动按钮 | [widgets/eval-008-floating-button.md](widgets/eval-008-floating-button.md) |
| W-009 | 输入框警告状态 | [widgets/eval-009-lineedit-alert.md](widgets/eval-009-lineedit-alert.md) |
| W-010 | 搜索输入框 | [widgets/eval-010-search-edit.md](widgets/eval-010-search-edit.md) |
| W-011 | 密码输入框 | [widgets/eval-011-password-edit.md](widgets/eval-011-password-edit.md) |
| W-012 | 数值输入框 | [widgets/eval-012-spinbox.md](widgets/eval-012-spinbox.md) |
| W-013 | 模糊效果控件 | [widgets/eval-013-blur-effect.md](widgets/eval-013-blur-effect.md) |
| W-014 | 进度条 | [widgets/eval-014-progress-bar.md](widgets/eval-014-progress-bar.md) |
| W-015 | 水波进度 | [widgets/eval-015-water-progress.md](widgets/eval-015-water-progress.md) |
| W-016 | 滑动条 | [widgets/eval-016-slider.md](widgets/eval-016-slider.md) |
| W-017 | 列表视图 | [widgets/eval-017-list-view.md](widgets/eval-017-list-view.md) |
| W-018 | 树形视图 | [widgets/eval-018-tree-view.md](widgets/eval-018-tree-view.md) |
| W-019 | 消息管理器 | [widgets/eval-019-message-manager.md](widgets/eval-019-message-manager.md) |
| W-020 | 标签前景色 | [widgets/eval-020-label-foreground.md](widgets/eval-020-label-foreground.md) |
| W-021 | 工具提示 | [widgets/eval-021-tooltip.md](widgets/eval-021-tooltip.md) |
| W-022 | 容器框架 | [widgets/eval-022-container-frame.md](widgets/eval-022-container-frame.md) |
| W-023 | 导航控件 | [widgets/eval-023-navigation.md](widgets/eval-023-navigation.md) |
| W-024 | 列表项委托 | [widgets/eval-024-item-delegate.md](widgets/eval-024-item-delegate.md) |
| W-025 | 应用单实例 | [widgets/eval-025-application-single.md](widgets/eval-025-application-single.md) |
| W-026 | 文件对话框 | [widgets/eval-026-file-dialog.md](widgets/eval-026-file-dialog.md) |
| W-027 | 关于对话框 | [widgets/eval-027-about-dialog.md](widgets/eval-027-about-dialog.md) |
| W-028 | 设置对话框 | [widgets/eval-028-settings-dialog.md](widgets/eval-028-settings-dialog.md) |
| W-029 | 下拉选择框 | [widgets/eval-029-combobox.md](widgets/eval-029-combobox.md) |
| W-030 | 应用身份与翻译加载 | [widgets/eval-030-application-translation.md](widgets/eval-030-application-translation.md) |

### declarative/ - QML 控件

| 编号 | 测试场景 | 文件 |
|------|----------|------|
| Q-001 | QML 中使用 dci 图标 | [declarative/eval-001-qml-dci-icon.md](declarative/eval-001-qml-dci-icon.md) |
| Q-002 | QML 对话框 | [declarative/eval-002-qml-dialog.md](declarative/eval-002-qml-dialog.md) |
| Q-003 | QML 按钮 | [declarative/eval-003-qml-button.md](declarative/eval-003-qml-button.md) |
| Q-004 | QML 输入控件 | [declarative/eval-004-qml-inputs.md](declarative/eval-004-qml-inputs.md) |
| Q-005 | QML 菜单 | [declarative/eval-005-qml-menu.md](declarative/eval-005-qml-menu.md) |
| Q-006 | QML 列表 | [declarative/eval-006-qml-list.md](declarative/eval-006-qml-list.md) |
| Q-007 | QML 进度条 | [declarative/eval-007-qml-progress.md](declarative/eval-007-qml-progress.md) |
| Q-008 | QML 滑动条 | [declarative/eval-008-qml-slider.md](declarative/eval-008-qml-slider.md) |
| Q-009 | QML 面板 | [declarative/eval-009-qml-panel.md](declarative/eval-009-qml-panel.md) |
| Q-010 | QML 视觉效果 | [declarative/eval-010-qml-effects.md](declarative/eval-010-qml-effects.md) |
| Q-011 | QML 取色器 | [declarative/eval-011-qml-color-selector.md](declarative/eval-011-qml-color-selector.md) |
| Q-012 | QML 全局对象 | [declarative/eval-012-qml-global.md](declarative/eval-012-qml-global.md) |

### theme/ - 主题系统

| 编号 | 测试场景 | 文件 |
|------|----------|------|
| T-001 | 控件颜色跟随主题切换 | [theme/eval-001-theme-palette.md](theme/eval-001-theme-palette.md) |
| T-002 | dci 图标动画 | [theme/eval-002-dci-icon-animation.md](theme/eval-002-dci-icon-animation.md) |
| T-003 | builtin 图标 | [theme/eval-003-builtin-icon.md](theme/eval-003-builtin-icon.md) |
| T-004 | 主题切换监听 | [theme/eval-004-theme-switch.md](theme/eval-004-theme-switch.md) |
| T-005 | Chameleon 风格理解 | [theme/eval-005-chameleon-style.md](theme/eval-005-chameleon-style.md) |
| T-006 | 控件调色板 | [theme/eval-006-palette-helper.md](theme/eval-006-palette-helper.md) |
| T-007 | 字体大小管理 | [theme/eval-007-font-size.md](theme/eval-007-font-size.md) |
| T-008 | DCI 图标按规范查找 | [theme/eval-008-dci-name-lookup.md](theme/eval-008-dci-name-lookup.md) |

### config/ - DConfig 配置

| 编号 | 测试场景 | 文件 |
|------|----------|------|
| C-001 | 使用 DConfig 存储配置 | [config/eval-001-dconfig-basic.md](config/eval-001-dconfig-basic.md) |
| C-002 | DConfig 元数据配置 | [config/eval-002-dconfig-meta.md](config/eval-002-dconfig-meta.md) |
| C-003 | DConfig 覆盖机制 | [config/eval-003-dconfig-override.md](config/eval-003-dconfig-override.md) |
| C-004 | DConfig 调试 | [config/eval-004-dconfig-debug.md](config/eval-004-dconfig-debug.md) |
| C-005 | 区分 appId 与配置 ID | [config/eval-005-dconfig-identifiers.md](config/eval-005-dconfig-identifiers.md) |
| C-006 | 插件场景 DConfig appId 与 configId 命名 | [config/eval-006-dconfig-plugin.md](config/eval-006-dconfig-plugin.md) |

### utilities/ - 工具类

| 编号 | 测试场景 | 文件 |
|------|----------|------|
| U-001 | DBus 通信 | [utilities/eval-001-dbus-call.md](utilities/eval-001-dbus-call.md) |
| U-002 | 桌面服务 | [utilities/eval-002-desktop-services.md](utilities/eval-002-desktop-services.md) |
| U-003 | 系统信息 | [utilities/eval-003-sysinfo.md](utilities/eval-003-sysinfo.md) |
| U-004 | 窗口管理器 | [utilities/eval-004-window-manager.md](utilities/eval-004-window-manager.md) |
| U-005 | 日志管理 | [utilities/eval-005-log-manager.md](utilities/eval-005-log-manager.md) |
| U-006 | 通知发送 | [utilities/eval-006-notify-sender.md](utilities/eval-006-notify-sender.md) |

### debugging/ - 调试场景

| 编号 | 测试场景 | 文件 |
|------|----------|------|
| D-001 | 调试主题问题 | [debugging/eval-001-debug-theme.md](debugging/eval-001-debug-theme.md) |
| D-002 | 调试风格问题 | [debugging/eval-002-debug-style.md](debugging/eval-002-debug-style.md) |
| D-003 | 调试图标问题 | [debugging/eval-003-debug-icon.md](debugging/eval-003-debug-icon.md) |
| D-004 | 调试 DConfig 问题 | [debugging/eval-004-debug-dconfig.md](debugging/eval-004-debug-dconfig.md) |
| D-005 | 调试窗口问题 | [debugging/eval-005-debug-window.md](debugging/eval-005-debug-window.md) |

### custom-controls/ - 自定义控件

| 编号 | 测试场景 | 文件 |
|------|----------|------|
| X-001 | 自定义控件风格 | [custom-controls/eval-001-custom-widget-style.md](custom-controls/eval-001-custom-widget-style.md) |
| X-002 | 自定义按钮 | [custom-controls/eval-002-custom-button.md](custom-controls/eval-002-custom-button.md) |
| X-003 | 自定义委托 | [custom-controls/eval-003-custom-delegate.md](custom-controls/eval-003-custom-delegate.md) |
| X-004 | 自定义控件主题感知 | [custom-controls/eval-004-custom-widget-theme.md](custom-controls/eval-004-custom-widget-theme.md) |
| X-005 | QML 自定义样式 | [custom-controls/eval-005-qml-custom-style.md](custom-controls/eval-005-qml-custom-style.md) |
| X-006 | StyleOption 使用 | [custom-controls/eval-006-style-option.md](custom-controls/eval-006-style-option.md) |

### project-setup/ - 工程配置

| 编号 | 测试场景 | 文件 |
|------|----------|------|
| P-001 | CMake 配置 DTK6 依赖 | [project-setup/eval-001-cmake-dtk6.md](project-setup/eval-001-cmake-dtk6.md) |

### architecture/ - 架构理解

| 编号 | 测试场景 | 文件 |
|------|----------|------|
| A-001 | DTK 模块关系 | [architecture/eval-001-module-relation.md](architecture/eval-001-module-relation.md) |
| A-002 | 调色板系统架构 | [architecture/eval-002-palette-architecture.md](architecture/eval-002-palette-architecture.md) |
| A-003 | 字体系统架构 | [architecture/eval-003-font-architecture.md](architecture/eval-003-font-architecture.md) |
| A-004 | 图标系统架构 | [architecture/eval-004-icon-architecture.md](architecture/eval-004-icon-architecture.md) |

### platform/ - 平台抽象

| 编号 | 测试场景 | 文件 |
|------|----------|------|
| L-001 | 窗口圆角设置 | [platform/eval-001-window-radius.md](platform/eval-001-window-radius.md) |
| L-002 | 窗口模糊效果 | [platform/eval-002-window-blur.md](platform/eval-002-window-blur.md) |
| L-003 | 窗口动效设置 | [platform/eval-003-window-effect.md](platform/eval-003-window-effect.md) |

## 运行测试

使用 Codex 运行 evals 测试：

```bash
codex --eval dtk-development/evals/widgets/eval-001-dialog-warning.md
```

或批量运行：

```bash
for dir in widgets declarative theme config utilities debugging custom-controls project-setup architecture platform; do
  for eval in dtk-development/evals/$dir/eval-*.md; do
    codex --eval "$eval"
  done
done
```

## 验证方法

每个 eval 文件包含：
- **任务描述**：具体的开发任务
- **期望输出**：代码应具备的特征
- **验证要点**：检查清单

测试时：
1. 给 Codex 提供任务描述
2. 检查输出是否符合期望
3. 对照验证要点逐一确认

## 添加新 Eval

新增 eval 时：
1. 复制模板 `eval-template.md`
2. 放入对应目录，命名为 `eval-NNN-description.md`
3. 填写任务、期望输出、验证要点
4. 更新本 README 的列表

## 触发评估

`trigger-evals.json` 包含 39 条触发测试（23 正例 + 16 反例），验证 `$dtk-development` 的触发准确性。

## 总计

共 **82** 个 output-quality evals（含 eval-template.md），覆盖 DTK 开发的核心场景。
