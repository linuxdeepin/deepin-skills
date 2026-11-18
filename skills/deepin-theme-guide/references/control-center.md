# 控制中心可见性与原生切换

## 安装与列举

`install --execute` 默认完成以下安装集成，不切换当前桌面：

| 资源 | 安装/注册位置 | 验证依据 |
| --- | --- | --- |
| 完整包 | `~/.local/share/uos-theme-personalize/themes/<id>` | manifest 与安装清单摘要 |
| 整体主题卡片 | `${XDG_CONFIG_HOME:-~/.config}/dde-appearance/deepin-themes/<id>/index.theme` 和封面 | Appearance `List("globaltheme")` |
| 图标及编译光标 | `${XDG_DATA_HOME:-~/.local/share}/icons/<id>`；有光标时完整镜像到 `~/.icons/<id>` | 两处资源相同，GTK/Qt 查找、DDE 光标扫描、libXcursor 加载 |
| 自定义壁纸 | 系统服务 `SaveCustomWallPaper` 返回的路径 | `GetCustomWallPapers(当前用户)`，与控制中心壁纸页同源 |

整体主题索引包含 `[Deepin Theme]`、名称、说明、Example、DefaultTheme/DarkTheme 与实际提供的组件；不写锁屏、字体、透明度等未请求字段。封面优先使用配套壁纸，没有图片时生成可识别 PNG 色卡。屏保仍通过 `activate --screensaver` 管理，Deepin 原生主题卡片不承载图片屏保设置。

图标索引保留 Directories 和 bloom,hicolor 回退；光标另有无 Directories 的 `cursor.theme`、有效的 `cursors/left_ptr` 和多档 Xcursor。两处目录不得只各放一类资源：Qt 会先读 ~/.icons 的 index.theme；DDE 的光标切换会先从 ~/.local/share/icons 同名目录找 cursor.theme。旧分拆布局可能导致 Qt 回退系统图标，DDE 只更新光标属性却未触发 XSettings/WM 热更新。

```bash
python3 "<技能目录>/scripts/theme_pack.py" install --package /绝对路径/主题包
python3 "<技能目录>/scripts/theme_pack.py" install --package /绝对路径/主题包 --execute
python3 "<技能目录>/scripts/theme_pack.py" desktop-status --id 主题id
python3 "<技能目录>/scripts/theme.py" catalog --kind globaltheme
```

DDE 对图标目录变更有约 10 秒的合并延迟，安装最多等待 15 秒读回列表。`installed=true,ok=false` 应检查 desktop_integration，稍后用 desktop-status 复核，不能重复覆盖安装或自动重启服务。

Deepin 25 控制中心自定义壁纸页直接调用系统 Daemon1 的列表接口，Appearance1 的 background 列表可能仍缓存旧值。`desktop-status` 的 background.listed 来自前者；session_catalog_listed 单列旧接口状态，不把后者的缓存误报成导入失败。

## 壁纸导入、更新与清理

使用运行时探测到的 `org.deepin.dde.Daemon1`（或受支持旧接口）。新接口 SaveCustomWallPaper 的参数是用户名、Unix FD、custom 类型；Gio 辅助进程通过 UnixFDList 传递真实打开的图片文件。不能把文件路径或普通整数当成 FD，不手写 `/var/cache/wallpapers`，不使用 sudo。系统 Python 缺少 Gio 时报告缺失能力，不安装依赖或声称已入库。

导入前记录该用户已有壁纸；内容相同的已有图片直接复用，不在卸载时删除。新导入的路径、摘要与进度保存在安装记录，失败时恢复；中断后可按内容摘要识别本次新图片。生成时文件名含内容摘要，更新图片时生成新包 ID，不覆盖同 URI 的旧图片再期望桌面刷新。

卸载前检查原生主题、图标、光标与各工作区壁纸是否仍在使用；控制中心手动选中的资源也会阻止删除。只删除本次新导入、摘要仍匹配的壁纸；多个技能包共用时将清理责任转交仍安装的包，最后一个包卸载时才清理。用户之后修改过的图片和安装目录会保留并报告问题。

`--no-desktop-integration` 只适合无桌面的离线测试，不能用于“控制中心可见”的交付。旧版包不自动原地迁移；从规范和原素材生成新 ID，保留旧恢复点。原来的目录中已被手写追加文件时，不能删除状态记录或更新摘要来伪装为未修改。

## 切换验收

正常切换使用控制中心或 DDE `Set("cursor", id)`，由原生服务更新 GTK、实时 XSettings、窗口管理器及 XFixes。X11 验证同时读取 Appearance CursorTheme、XSettings1 的 Gtk/CursorThemeName 与 WM cursorTheme，再按主题名加载各尺寸/状态和包内像素摘要比较。旧 GSettings、kcminputrc、xrdb 单列 legacy_layers，不能单凭旧 schema 值推断实时指针失败。Wayland 不运行 X11 写入，不能把 X11 验证结果外推为 Wayland 热更新保证。

`--cursor-sync` 是旧配置修复选项，不是日常点击切换的必要步骤。不要安装监听后台程序持续覆盖用户后续选择，也不通过自动注销或重启应用制造生效。

图标验收包含 GTK3 三档查找和 Qt6 三档真实加载来源，独立报告 lookup_verified 与 qt_runtime.lookup_verified，runtime_verified 仅在两者通过时为真。Qt 辅助源码随技能分发，仅用本机已有开发工具在临时目录构建；缺少工具或无法解析 Qt 来源时明确未验证。视觉观察仍独立报告，不把列表可见、配置读回或加载成功当作风格质量验收。

官方实现依据：[DDE 主题路径与原生鼠标热更新](https://github.com/linuxdeepin/dde-appearance/blob/master/src/service/modules/api/themes.cpp)、[主题扫描格式](https://github.com/linuxdeepin/dde-appearance/blob/master/src/service/modules/subthemes/scanner.cpp)、[目录变更合并](https://github.com/linuxdeepin/dde-appearance/blob/master/src/service/impl/fsnotify.cpp)、[壁纸导入 FD 接口](https://github.com/linuxdeepin/dde-appearance/blob/master/src/service/dbus/appearancedbusproxy.cpp)、[控制中心自定义壁纸列举](https://github.com/linuxdeepin/dde-control-center/blob/master/src/plugin-personalization/operation/wallpaperprovider.cpp)。目标机实际 introspection 和读回优先。
