# deepin Skills

[简体中文](README.md)

deepin Skills organizes framework knowledge, plugin APIs, engineering guidance, and evaluation cases into on-demand skills for building native deepin/UOS applications and DDE desktop plugins. They are intended for AI coding agents that can read `SKILL.md`.

No prior programming experience is required. Designers can describe interfaces and interactions, project managers can state product goals and acceptance criteria, and developers can request implementation or debugging help. The agent selects the relevant skill, reads the related references, and assists with creating, changing, and maintaining project code. Experienced developers can also use the skills as technical references for deepin platform development.

## Installation

Choose one method to install all skills into `${SKILL_HOME:-~/.agents}/skills`.

One-line installation:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/linuxdeepin/deepin-skills/master/scripts/install.sh)
```

Local installation:

```bash
./scripts/install.sh
```

Force replacement with one-line installation:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/linuxdeepin/deepin-skills/master/scripts/install.sh) --force
```

For a local checkout, use `./scripts/install.sh --force`.

## Quick Start

After installation, open the target project in an AI coding agent that supports skills and describe the task in natural language. The agent selects the relevant skill and reads only the references needed for the task.

- A designer can ask: "Design a settings window for a deepin desktop application with Account, Notifications, and Appearance pages, then implement the interface and interactions using DTK conventions."
- A project manager can ask: "Create a taskbar network-status plugin. It should show a quick panel when clicked, display the current connection state, and open the relevant system settings."
- A developer can ask: "Add a system settings module to DDE Control Center with page navigation, configuration persistence, and D-Bus data interactions."

## Maintained Skills

Choose a skill according to the target system version:

| Skill | Supported system versions | Purpose |
| --- | --- | --- |
| [`dtk-development`](skills/dtk-development/SKILL.md) | deepin/UOS v25 | Use this skill to build and maintain native deepin/UOS desktop applications with DTK. It covers understanding DTK architecture, module boundaries, and module responsibilities; selecting QWidget or QML UI stacks; theme, icon, and DConfig integration; D-Bus, notifications, and single-instance behavior; plus CMake setup, window effects, X11 and Wayland platform adaptation, and DTK source debugging. |
| [`dde-shell-development`](skills/dde-shell-development/SKILL.md) | deepin/UOS v25 | Use this skill to extend DDE Shell desktop surfaces such as the Dock, top bar, sidebars, and other panels. It guides the selection and implementation of Applet, Containment, and Panel plugins; QML and C++ integration; plugin lifecycle and loading; and LayerShell windows anchored to screen edges on Wayland. |
| [`dde-control-center-development`](skills/dde-control-center-development/SKILL.md) | deepin/UOS v25 | Use this skill to build system settings modules and plugins for DDE Control Center. It covers the module tree, navigation, and search architecture; C++ and QML APIs for settings pages; D-Bus and data interactions; plus plugin builds, translations, packaging, installation, and local debugging. |
| [`dde-tray-development`](skills/dde-tray-development/SKILL.md) | deepin/UOS v25 | Use this skill to create DDE taskbar tray plugins, quick-panel controls, and related interactions that follow DDE desktop conventions. It covers tray plugin interfaces and loading behavior, status and messaging protocols, context menus, quick-panel detail pages, and integration points such as taskbar position changes for stable, well-integrated taskbar plugins. |
| [`dde-grand-search-development`](skills/dde-grand-search-development/SKILL.md) | deepin/UOS v25 | Use this skill to build extension search plugins for Grand Search, so that third-party application data and results appear in the deepin global search window. It covers the DBus-service integration model, `.conf` configuration and the Auto/Manual/Trigger run modes, the V1.0 Search/Stop/Action protocol and result JSON format, group and item name internationalization, CMake builds and Debian packaging, and troubleshooting for plugins that are not loaded or return no results. |

## Community Events

This project has participated in the following community events:

| Event | Start date | End date |
| --- | --- | --- |
| [1 Billion Token Prize Pool: Build Your Own deepin Desktop Plugin](https://bbs.deepin.org/post/300665) | 2026-08-10 | 2026-09-14 |

## Repository Layout

All public skills are grouped under `skills/`, and the installer is stored in `scripts/`:

```text
deepin-skills/
├── skills/
│   ├── dtk-development/
│   ├── dde-shell-development/
│   ├── dde-control-center-development/
│   ├── dde-tray-development/
│   └── dde-grand-search-development/
└── scripts/
    └── install.sh
```

See the [contribution guide](CONTRIBUTING_EN.md) for each skill's directory layout and maintenance requirements.

## Getting help

For usage questions, ask the community through:

- [Telegram group](https://t.me/deepin)
- [Matrix](https://matrix.to/#/#deepin-community:matrix.org)
- [Forum](https://bbs.deepin.org)
- [Wiki](https://wiki.deepin.org/)

## Getting involved

We encourage you to report issues and contribute changes. Read the repository-specific [contribution guide](CONTRIBUTING_EN.md) first.

- [Contribution guide for developers](https://github.com/linuxdeepin/developer-center/wiki/Contribution-Guidelines-for-Developers-en)

## License

deepin-skills is licensed under [LGPL-3.0-or-later](LICENSE).
