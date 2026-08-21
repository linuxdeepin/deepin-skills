# Eval: 创建快捷面板插件

## 任务

用户想创建一个快捷面板插件，同时有托盘图标和快捷面板控件。

指导用户使用 Type_Quick 标志和 QUICK_ITEM_KEY。

## 期望输出

回答应：
1. 展示 flags() 设置 Type_Quick | Quick_Panel_Full
2. 展示 itemWidget 处理 QUICK_ITEM_KEY
3. 展示控件尺寸设置
4. 说明正确的 DConfig 元数据路径，并使用 `dde-dconfig` 注册自定义插件

## 验证要点

- [ ] flags() 使用 Type_Quick（非 Type_Tray）
- [ ] Quick_Panel_Single/Multi/Full 布局标志
- [ ] itemWidget(Dock::QUICK_ITEM_KEY) 返回快捷面板控件
- [ ] setFixedHeight(Dock::QUICK_ITEM_HEIGHT)
- [ ] 配置元数据路径为 `/usr/share/dsg/configs/org.deepin.dde.shell/org.deepin.ds.dock.tray.json`
- [ ] 使用 App ID `org.deepin.dde.shell`、Resource `org.deepin.ds.dock.tray` 和 Key `quickPlugins`
- [ ] 使用 `dde-dconfig` 读取现有列表，并在保留已有值的前提下添加 `pluginName()`

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 所有验证要点全部满足，代码可编译或语法正确 |
| ⚠️ **PARTIAL** | 核心功能满足（第 1-2 项），但边缘检查项未通过 |
| ❌ **FAIL** | 核心功能未实现，或使用了禁止的模式

## 反模式检查
- [ ] Type_Tray 与 Type_Quick 未互斥使用
- [ ] 快捷面板未选 Quick_Panel_* 布局标志
- [ ] 未将 App ID 误写为 `org.deepin.ds.dock`（正确为 `org.deepin.dde.shell`，写错时注册静默无效）
