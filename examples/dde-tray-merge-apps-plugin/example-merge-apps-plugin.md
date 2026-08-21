# 示例：合并应用图标快捷开关插件（dde-tray-merge-apps）

这是一个**独立、可 debian 打包**、**不依赖 dde-dock** 的快捷面板插件示例，用来完整
演示 dde-tray-loader V2 插件的开发流程。插件在快捷面板与托盘同时显示，单击任意一处
即可切换控制中心「个性化 → 桌面和任务栏」的「合并应用图标」开关，并支持右键菜单
打开控制中心跳转到该设置页。

**完整项目（含源码、CMake、翻译、debian 打包与开发流程 README）位于
`assets/examples/merge-apps-plugin/`，可直接复制使用。**

## 需求与能力映射

| 需求 | 实现方式 |
|------|----------|
| 在快捷面板显示 | `flags()` 返回 `Type_Quick | Quick_Panel_Full`，`itemWidget(Dock::QUICK_ITEM_KEY)` 返回快捷面板控件 |
| 在快捷面板显示信息 | 快捷面板控件显示图标 + 名称 + 状态（已合并/未合并） |
| 单击切换合并应用开关 | 托盘控件与快捷面板控件 `clicked` 信号 → `MergeAppsController::setMergeApps()` |
| 右键打开控制中心 | `itemContextMenu()` + `invokedMenuItem()`，用 `dde-am` 打开并跳转 `personalization/dock` |
| 独立项目 + debian 打包 | 独立 `CMakeLists.txt` + `debian/` 打包目录，不依赖 dde-dock |

## 关键实现要点

### 1. 依赖与命名

- 项目/插件名：`dde-tray-merge-apps`（`pluginName()` 返回值，也是 `.so`、翻译
  basename、`quickPlugins` 条目）
- 只依赖 `dde-tray-loader-dev`（pkg-config `dde-tray-loader`），**不依赖 dde-dock**
- 安装到 dde-tray-loader 固定插件目录 `/usr/lib/dde-dock/plugins/`

### 2. 开关的底层存储

「合并应用图标」底层是 DConfig，与 dde-shell taskmanager 一致：

- AppId：`org.deepin.dde.shell`
- 配置 ID：`org.deepin.ds.dock.taskmanager`
- 键：`noTaskGrouping`（bool），`combineApp = !noTaskGrouping`

### 3. 接口与 IID

```cpp
class MergeAppsPlugin : public QObject, public PluginsItemInterfaceV2
{
    Q_OBJECT
    Q_INTERFACES(PluginsItemInterfaceV2)
    Q_PLUGIN_METADATA(IID ModuleInterface_iid_V2 FILE "dde-tray-merge-apps-plugin.json")
};
```

### 4. 翻译（dtk-development 规则）

在 `init()` 中、创建可翻译文本之前调用
`DGuiApplicationHelper::loadTranslator(pluginName(), pluginName(), { QLocale::system() })`，
从 `/usr/share/dde-tray-merge-apps/translations/dde-tray-merge-apps_<locale>.qm` 加载
并处理语言回退。CMake 用 `lrelease` 编译 `translations/*.ts` 并安装 `.qm`。

## 安装与注册

```bash
# 构建（依赖 dde-tray-loader-dev、Qt6、DTK6）
cmake -B build -DCMAKE_INSTALL_PREFIX=/usr
cmake --build build
sudo cmake --install build   # 安装到 /usr/lib/dde-dock/plugins/ + 翻译目录
```

快捷面板只显示 `pluginName()` 出现在 DConfig `quickPlugins`（AppId
`org.deepin.dde.shell`、资源 `org.deepin.ds.dock.tray`）中的插件。该键**默认只读**，
`dde-dconfig set` 会被忽略。注册步骤：

1. （仅当仍只读）把
   `/usr/share/dsg/configs/org.deepin.dde.shell/org.deepin.ds.dock.tray.json` 里
   `quickPlugins` 的 `permissions` 改为 `readwrite`，重启 `dde-dconfig-daemon`。
2. `dde-dconfig set -a org.deepin.dde.shell -r org.deepin.ds.dock.tray -k quickPlugins
   -v '["...已有插件...","dde-tray-merge-apps"]'`（保留已有项，末尾追加）。
3. `dde-dconfig get ...` 校验含 `dde-tray-merge-apps`，注销/重新登录或重启任务栏生效。

## 参考

- 快捷面板布局与注册：`quick-panel-guide.md`
- 右键菜单协议：`context-menu.md`
- 接口规范：`tray-plugin-spec.md`
- 翻译规则：`$dtk-development`（`DGuiApplicationHelper::loadTranslator`）
