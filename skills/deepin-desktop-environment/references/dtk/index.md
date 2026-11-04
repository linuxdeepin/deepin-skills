# DTK 用户配置与系统查询

这里收录 DTK 应用偏好、系统区域格式，以及 DTK 提供的命令行工具集。DTK 应用偏好作用于 DTK 应用，区域格式作用于系统全局；命令行工具涵盖系统信息查询、中文转拼音、DCI 图标处理、DConfig 代码生成、DBus XML 转换、设置翻译生成、SVG 转换和窗口调试等开发辅助功能。

## 公开配置

- [DTK 应用偏好](config/org.deepin.dtk.preference.md)：主题、动画、滚动条、标题栏和菜单等应用偏好。
- [系统区域格式](config/org.deepin.region-format.md)：日期、时间、数字、货币和纸张格式。

## 工具

- [deepin-gui-settings](cli/deepin-gui-settings.md)：查询和修改 X11 窗口属性，使用前确认平台和目标窗口。
- [deepin-os-release](cli/deepin-os-release.md)：只读查询系统信息。
- [ch2py](cli/ch2py.md)：中文转拼音；不是桌面语言切换工具。
- [dci](cli/dci.md)：DCI 文件打包/解包/查看工具。
- [dconfig2cpp](cli/dconfig2cpp.md)：DConfig JSON 配置转 C++ 代码生成器。
- [qdbusxml2cpp-fix](cli/qdbusxml2cpp-fix.md)：DTK 修复版 DBus XML 转 C++ 代码生成器。
- [dtk-settings](cli/dtk-settings.md)：DTK 设置翻译和 GSettings schema 生成工具。
- [dci-iconfinder](cli/dci-iconfinder.md)：在图标主题中查找 DCI 图标文件路径。
- [dci-icon-theme](cli/dci-icon-theme.md)：从普通图标批量生成 DCI 图标文件。
- [dde-kwin-bug](cli/dde-kwin-bug.md)：DDE KWin 窗口启动和渲染调试工具。
- [dtk6-svgc](cli/dtk6-svgc.md)：SVG 转 PNG 转换工具。
