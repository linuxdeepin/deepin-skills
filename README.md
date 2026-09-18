# deepin Skills

[English](README_EN.md)

deepin Skills 面向 deepin/UOS 原生应用和 DDE 桌面插件开发，将框架知识、插件接口、工程实践和评估用例组织为可按需加载的 Skill，供支持读取 `SKILL.md` 的 AI 编程 Agent 使用。

使用者无需预先具备编程经验。设计师可以描述界面和交互，项目经理可以说明产品目标和验收要求，研发人员可以提出具体的实现或排查任务；Agent 会根据任务选择对应的 Skill，读取相关参考资料，并协助创建、修改和维护项目代码。经验丰富的开发者也可以将 Skill 作为 deepin 平台开发的技术参考。

## 安装

任选一种方式安装所有 skill 到 `${SKILL_HOME:-~/.agents}/skills`。

一键安装：

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/linuxdeepin/deepin-skills/master/scripts/install.sh)
```

本地安装：

```bash
./scripts/install.sh
```

一键强制覆盖：

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/linuxdeepin/deepin-skills/master/scripts/install.sh) --force
```

本地强制覆盖使用 `./scripts/install.sh --force`。

## 快速开始

安装后，在支持 Skill 的 AI 编程 Agent 中打开目标项目，直接用自然语言描述要完成的任务。Agent 会根据任务选择对应的 Skill，并按需读取相关参考资料。

- 设计师可以提出：“为 deepin 桌面应用设计一个设置窗口，包含账户、通知和外观三个页面，并按 DTK 规范实现界面和交互。”
- 项目经理可以提出：“为任务栏开发一个网络状态插件，点击后显示快捷面板，支持查看当前连接状态和打开系统设置。”
- 研发人员可以提出：“在 DDE 控制中心中新增一个系统设置模块，包含页面导航、配置保存和 D-Bus 数据交互。”

## 当前维护的 Skill

请根据目标系统版本选择 skill：

| Skill | 适用系统版本 | 用途 |
| --- | --- | --- |
| [`dtk-development`](skills/dtk-development/SKILL.md) | deepin/UOS v25 | 用于开发和维护基于 DTK 的 deepin/UOS 原生桌面应用。适合需要理解 DTK 架构、模块划分和各模块职责，选择 QWidget 或 QML 技术栈并构建界面，实现主题、图标和 DConfig 配置，以及接入 D-Bus、通知、单实例等系统服务的场景；同时覆盖 CMake 工程配置、窗口效果、X11 与 Wayland 平台适配和 DTK 源码调试。 |
| [`dde-shell-development`](skills/dde-shell-development/SKILL.md) | deepin/UOS v25 | 用于扩展 DDE Shell 的桌面能力，例如 Dock、顶栏、侧栏和其他面板区域。该 skill 指导开发者选择并实现 Applet、Containment 或 Panel 插件，处理 QML 与 C++ 集成、插件生命周期和加载机制，并支持使用 LayerShell 创建贴靠屏幕边缘的 Wayland 窗口。 |
| [`dde-control-center-development`](skills/dde-control-center-development/SKILL.md) | deepin/UOS v25 | 用于为 DDE 控制中心开发系统设置模块和插件。适合需要理解模块树、导航和搜索机制，使用控制中心的 C++ 或 QML API 构建设置页面，处理 D-Bus 与数据交互，以及完成插件构建、翻译、打包、安装和本地调试的开发任务。 |
| [`dde-tray-development`](skills/dde-tray-development/SKILL.md) | deepin/UOS v25 | 用于开发符合 DDE 桌面交互方式的任务栏托盘插件、快捷面板控件及相关交互功能。该 skill 覆盖托盘插件接口和加载行为、状态与消息协议、右键菜单、快捷面板详情页，以及任务栏位置变化等集成场景，帮助开发者实现稳定、规范的任务栏插件。 |
| [`dde-grand-search-development`](skills/dde-grand-search-development/SKILL.md) | deepin/UOS v25 | 用于为全局搜索开发扩展搜索插件，让第三方应用的数据和搜索结果出现在 deepin 全局搜索界面中。该 skill 覆盖插件以 DBus 服务接入的机制、`.conf` 配置与 Auto/Manual/Trigger 运行模式、V1.0 协议的 Search/Stop/Action 接口与结果 JSON 格式、分组与结果名国际化、CMake 构建与 Debian 打包，以及插件未加载、搜索无结果等常见故障的排查方法。 |

## 示例项目

`examples/` 目录收录使用本仓库 Skill 生成的完整项目，用于展示 Skill 在实际开发任务中的使用方式和产出结果。示例项目包含可构建的源码及必要的工程文件，可用于学习、验证和回归相关开发规范。

| 示例 | 使用的 Skill | 说明 |
| --- | --- | --- |
| [DTK Code Viewer](https://github.com/linuxdeepin/deepin-skills/tree/master/examples/dtk-codeviewer) | `dtk-development` | 一个基于 DTK6 和 QWidget 的代码及文本文件查看器。示例覆盖 DTK 应用生命周期、单实例、标签页、文件对话框、大文件分块加载、主题与 DCI 图标、DConfig、日志、翻译、CMake 安装和 Debian 打包。 |

每个示例的依赖、构建命令和功能说明见示例目录中的 README。

## 社区活动

本项目参与过以下社区活动：

| 活动 | 开始时间 | 结束时间 |
| --- | --- | --- |
| [10 亿 Token 奖池：写出属于你的 deepin 桌面插件](https://bbs.deepin.org/post/300665) | 2026-08-10 | 2026-09-14 |

## 目录结构

仓库将所有对外 skill 集中在 `skills/`，使用 Skill 生成的项目位于 `examples/`，安装脚本位于 `scripts/`：

```text
deepin-skills/
├── skills/
│   ├── dtk-development/
│   ├── dde-shell-development/
│   ├── dde-control-center-development/
│   ├── dde-tray-development/
│   └── dde-grand-search-development/
├── examples/
│   └── dtk-codeviewer/
└── scripts/
    └── install.sh
```

每个 skill 的目录结构和维护要求见[贡献说明](CONTRIBUTING.md)。

## 获取帮助

使用中遇到问题，可通过以下社区渠道寻求帮助：

- [Telegram 群组](https://t.me/deepin)
- [Matrix](https://matrix.to/#/#deepin-community:matrix.org)
- [论坛](https://bbs.deepin.org)
- [Wiki](https://wiki.deepin.org/)

## 参与贡献

欢迎报告问题并贡献改动。请先阅读本仓库的 [贡献说明](CONTRIBUTING.md)。

- [开发者贡献指南](https://github.com/linuxdeepin/developer-center/wiki/Contribution-Guidelines-for-Developers)

## 许可证

deepin-skills 使用 [LGPL-3.0-or-later](LICENSE) 许可证。
