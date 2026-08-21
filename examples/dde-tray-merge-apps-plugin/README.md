# dde-tray-merge-apps：合并应用图标快捷开关插件示例

这是一个**独立、完整可打包**的 dde-tray-loader 托盘插件示例，用于演示 dde-tray-loader
快捷面板插件的完整开发流程。插件在**快捷面板**与**托盘区**同时显示，单击任意一处
即可切换控制中心「个性化 → 桌面和任务栏」下的**合并应用图标**开关，并支持右键菜单
打开控制中心跳转到该设置页。

> 本项目**不依赖 dde-dock**，只依赖 `dde-tray-loader`（开发头文件 + 运行时）。
> 插件仍按 dde-tray-loader 的约定安装到其固定插件目录 `/usr/lib/dde-dock/plugins/`
> （该路径是 dde-tray-loader 扫描插件的位置，与 dde-dock 无关）。

功能清单：

- 在**快捷面板**中显示：图标 + 名称 + 当前状态（已合并 / 未合并）
- 单击**托盘图标**或**快捷面板控件**切换「合并应用图标」开关
- 右键菜单：
  - 「开启 / 关闭合并」直接切换开关
  - 「打开控制中心设置」通过 `dde-am` 打开控制中心并跳转到 `personalization/dock`
- 独立项目结构，支持 **debian 打包**
- 翻译按 **dtk-development 规则**加载（`DGuiApplicationHelper::loadTranslator`）

---

## 1. 功能原理

「合并应用图标」是控制中心「个性化 → 桌面和任务栏」里的一个开关。它底层存储在 DConfig：

| 项 | 值 |
|----|----|
| AppId | `org.deepin.dde.shell` |
| 配置 ID | `org.deepin.ds.dock.taskmanager` |
| 键 | `noTaskGrouping`（bool） |
| 语义 | `noTaskGrouping == false` ⇒ 合并应用图标（开启）；`true` ⇒ 不合并 |

控制中心读取时做 `combineApp = !noTaskGrouping`，本插件用同样的语义，从而与控制中心
完全同步，并通过 DConfig 的 `valueChanged` 信号监听外部改动。

控制中心对应模块页面 URL 为 `personalization/dock`（显示名「桌面和任务栏」），
右键菜单通过 `dde-am org.deepin.dde.control-center -- -p personalization/dock`
打开并跳转。

---

## 2. 项目结构

```
dde-tray-merge-apps-plugin/
├── CMakeLists.txt                        # 构建脚本（依赖 dde-tray-loader）
├── src/
│   ├── dde-tray-merge-apps-plugin.json   # 插件元数据（Q_PLUGIN_METADATA 加载）
│   ├── mergeappscontroller.{h,cpp}       # DConfig 开关封装（读写 + 变化监听）
│   ├── mergeappsplugin.{h,cpp}           # 插件主体：实现 PluginsItemInterfaceV2
│   ├── quickpanelwidget.{h,cpp}          # 快捷面板控件（显示信息 + 单击切换）
│   └── trayitemwidget.{h,cpp}            # 托盘图标控件（单击切换）
├── translations/
│   ├── dde-tray-merge-apps_en.ts         # 英文（与源文本一致）
│   ├── dde-tray-merge-apps_zh_CN.ts      # 简体中文
│   ├── dde-tray-merge-apps_zh_HK.ts      # 繁体中文（香港）
│   └── dde-tray-merge-apps_zh_TW.ts      # 繁体中文（台湾）
├── icons/                                # 亮/暗两套主题图标（-dark 后缀为暗色版）
│   ├── merge-apps-on.svg
│   ├── merge-apps-off.svg
│   ├── merge-apps-on-dark.svg
│   └── merge-apps-off-dark.svg
├── debian/                               # debian 打包所需文件
└── README.md
```

## 3. 开发流程

### 3.1 依赖安装

UOS v25（Qt6 / DTK6）环境：

```bash
sudo apt install cmake \
    qt6-base-dev qt6-svg-dev qt6-tools-dev qt6-l10n-tools \
    libdtk6widget-dev libdtk6gui-dev libdtk6core-dev \
    dde-tray-loader-dev
```

> 开发头文件由 `dde-tray-loader-dev` 提供（CMake 包 `DdeTrayLoader`，头文件目录
> 变量 `DDE_TRAY_LOADER_INCLUDE_DIR`），位于 `/usr/include/dde-dock/`
> （`pluginsiteminterface_v2.h`、`constants.h`、`pluginproxyinterface.h` 等）。
> **不依赖 dde-dock-dev。**

### 3.2 继承接口与 IID

```cpp
class MergeAppsPlugin : public QObject, public PluginsItemInterfaceV2
{
    Q_OBJECT
    Q_INTERFACES(PluginsItemInterfaceV2)
    Q_PLUGIN_METADATA(IID ModuleInterface_iid_V2 FILE "dde-tray-merge-apps-plugin.json")
    ...
};
```

`dde-tray-merge-apps-plugin.json` 中的 `"api": "2.0.0"` 是插件 API 版本，必须存在。

### 3.3 flags：声明为快捷面板插件

```cpp
Dock::PluginFlags flags() const override
{
    return Dock::Type_Quick | Dock::Quick_Panel_Full
            | Dock::Attribute_CanDrag | Dock::Attribute_CanInsert;
}
```

`Type_Tray` 与 `Type_Quick` 互斥；快捷面板控件只 `setFixedHeight(Dock::QUICK_ITEM_HEIGHT)`。

### 3.4 itemWidget 与注册

`init()` 中 `m_proxyInter->itemAdded(this, kTrayKey)` 注册托盘图标；快捷面板由
`itemWidget(Dock::QUICK_ITEM_KEY)` 提供，`itemWidget(kTrayKey)` 返回托盘控件。

### 3.5 开关读写与状态同步

`MergeAppsController` 封装 DConfig：

```cpp
m_config = DConfig::create("org.deepin.dde.shell",
                           "org.deepin.ds.dock.taskmanager", QString(), this);
bool noTaskGrouping = m_config->value("noTaskGrouping", false).toBool();
bool combine = !noTaskGrouping;              // 读取
m_config->setValue("noTaskGrouping", !combine); // 写入
connect(m_config, &DConfig::valueChanged, ...); // 监听外部改动
```

托盘单击、快捷面板单击、右键菜单项都调用 `toggleMergeApps()`；状态变化后刷新两个控件。

### 3.6 右键菜单与打开控制中心

`itemContextMenu()` 返回 JSON 菜单，`invokedMenuItem()` 处理点击。打开控制中心推荐用
`dde-am`（Wayland 下自动处理 xdg-activation token）：

```cpp
QStringList args{"--by-user", "org.deepin.dde.control-center", "--",
                 "-p", "personalization/dock"};
QProcess::startDetached("dde-am", args);
```

### 3.7 翻译（dtk-development 规则）

按 dtk-development 的规则加载翻译：

- 翻译文件 basename 与插件名一致：`dde-tray-merge-apps_<locale>.qm`
- 放在标准数据目录：`/usr/share/dde-tray-merge-apps/translations/`
- 在 `init()` 中、创建可翻译文本之前调用 `DGuiApplicationHelper::loadTranslator`，
  它会自动处理 `zh_CN -> zh` 的语言回退：

```cpp
void MergeAppsPlugin::initTranslator()
{
    DGuiApplicationHelper::loadTranslator(pluginName(), pluginName(),
                                          { QLocale::system() });
}
```

CMake 用 Qt6 标准的 `qt6_add_translations()`（`Qt6::LinguistTools`）在构建时把
`translations/*.ts` 编译为 `.qm` 并安装到上述目录。

## 4. 构建

```bash
cmake -B build -DCMAKE_INSTALL_PREFIX=/usr
cmake --build build
```

生成的动态库位于 `build/libdde-tray-merge-apps.so`。

## 5. 安装与注册（重要）

### 5.1 安装插件

```bash
sudo cmake --install build
# 安装 libdde-tray-merge-apps.so 到 /usr/lib/dde-dock/plugins/（dde-tray-loader 插件目录）
# 安装 .qm 到 /usr/share/dde-tray-merge-apps/translations/
# 安装亮/暗两套图标到 /usr/share/icons/hicolor/scalable/apps/
```

### 5.2 注册到快捷面板（`quickPlugins`，需先可写）

dde-shell 的快捷面板只显示 `pluginName()` 出现在 DConfig `quickPlugins` 中的插件。
读取该列表的配置为：AppId `org.deepin.dde.shell`、资源 `org.deepin.ds.dock.tray`、
键 `quickPlugins`。

> **默认该键是 `readonly`**，`dde-dconfig set` 会被静默忽略。需要先把它改成可写，
> 然后用 `dde-dconfig set` 追加插件名 `"dde-tray-merge-apps"`。

#### 5.2.1 仅当键仍为只读时：用 override 文件改为可写

旧版本中该键默认 `readonly`（新版本已默认 `readwrite`，可跳过本步）。不要直接编辑
`/usr/share/dsg/configs` 下的 vendor 元数据（包升级会被覆盖），应使用
`/etc/dsg/configs/overrides/` 下的覆盖文件（优先级最高）：

```bash
sudo tee /etc/dsg/configs/overrides/org.deepin.dde.shell/org.deepin.ds.dock.tray/10-merge-apps.json <<'EOF'
{
    "quickPlugins": {
        "permissions": "readwrite"
    }
}
EOF

sudo systemctl restart dde-dconfig-daemon   # 或注销重新登录
```

#### 5.2.2 追加 dde-tray-merge-apps 并写回

```bash
dde-dconfig get -a org.deepin.dde.shell -r org.deepin.ds.dock.tray -k quickPlugins

dde-dconfig set -a org.deepin.dde.shell -r org.deepin.ds.dock.tray \
    -k quickPlugins -v '["network","bluetooth",...,"sound","dde-tray-merge-apps"]'
```

> `dde-dconfig set` 会整体替换该值，必须带上查询到的全部已有插件名，再在末尾追加
> `"dde-tray-merge-apps"`。AppId 是 `org.deepin.dde.shell`（不是 `org.deepin.ds.dock`）。

#### 5.2.3 校验并重启任务栏

```bash
dde-dconfig get -a org.deepin.dde.shell -r org.deepin.ds.dock.tray -k quickPlugins
# 注销并重新登录，或：pkill -f dde-shell; pkill -f dde-tray-loader
```

### 5.3 验证

1. 确认插件已安装到 `/usr/lib/dde-dock/plugins/libdde-tray-merge-apps.so`，且
   `dde-tray-merge-apps` 已在 `quickPlugins` 中；
2. 确认快捷面板出现「合并应用图标」项，托盘出现对应图标；
3. 单击托盘 / 快捷面板 / 右键「开启/关闭合并」，再到控制中心确认开关状态一致；
4. 右键「打开控制中心设置」应跳转到「个性化 → 桌面和任务栏」；
5. 在控制中心手动切换该开关，观察插件显示是否同步刷新。

## 6. Debian 打包

`debian/` 目录已包含打包所需文件。在项目根目录执行：

```bash
dpkg-buildpackage -us -uc -b
```

生成 `dde-tray-merge-apps-plugin_1.0.0-1_amd64.deb`，安装：

```bash
sudo apt install ./dde-tray-merge-apps-plugin_1.0.0-1_amd64.deb
```

打包要点：

- `debian/rules` 通过 `override_dh_auto_configure` 指定 `CMAKE_INSTALL_PREFIX=/usr`，
  使插件安装到 `/usr/lib/dde-dock/plugins/`（dde-tray-loader 插件目录）；
- 无需 `debian/*.install`：debhelper 13 单二进制包会把 CMake 安装规则产出的
  文件（.so、.qm、图标）直接装入包内，不要引用不存在的 `debian/tmp` 路径；
- compat 版本只在 `debian/control` 的 `debhelper-compat (= 13)` 声明一次，
  不要再保留 `debian/compat` 文件；
- `debian/control` 的 `Build-Depends` 声明 `dde-tray-loader-dev`（不依赖
  `dde-dock-dev`），`Depends` 声明运行时依赖 `dde-tray-loader`。

---

## 常见问题

- **快捷面板不显示**：确认 `flags()` 含 `Type_Quick | Quick_Panel_*`、`dde-tray-merge-apps`
  已加入 `quickPlugins`（若键只读先改可写）、`itemWidget(Dock::QUICK_ITEM_KEY)` 返回了
  有效控件，且控件只设了 `setFixedHeight()`。
- **托盘图标不显示**：确认 `init()` 中调用了 `itemAdded(this, kTrayKey)` 且
  `itemWidget` 返回了托盘控件。
- **右键菜单不出现**：确认 `itemContextMenu` 返回了合法 JSON（含 `items` 数组），
  且 `invokedMenuItem` 处理了对应 `itemId`。
- **没有翻译**：确认 `/usr/share/dde-tray-merge-apps/translations/`
  `dde-tray-merge-apps_zh_CN.qm` 已安装（文件 basename 必须与插件名一致），并重启任务栏。
