# org.deepin.dtk QML 模块

org.deepin.dtk 是 dtkdeclarative 提供的 QML 声明式控件模块，为 DTK 应用提供一套完整的界面控件库。常见交互场景涵盖按钮、对话框与窗口、文本与数值输入、菜单与动作、列表与视图以及视觉效果与渲染，所有控件统一遵循 DTK 设计规范的主题色、圆角和交互反馈风格，可与 `org.deepin.dtk.style` 样式单例和 `org.deepin.dtk.settings` 设置模块配合使用。

## 集成

### 使用方式

QML 模块 URI 为 `org.deepin.dtk`，导入版本为 1.0。模块以动态插件形式发布，使用方无需安装额外模块包，确保系统已安装 dtkdeclarative 运行时库即可。

在 QML 文件中导入：

```qml
import org.deepin.dtk 1.0
```

导入后可使用模块中的所有控件类型。样式参数通过 `org.deepin.dtk.style` 子模块的单例设置，对话框控件通过 `org.deepin.dtk.settings` 子模块配置。

---

## 接口分类

- [按钮控件](org.deepin.dtk/buttons.md) — 提供图标按钮、语义化按钮、开关切换按钮、浮动操作按钮四种按钮类型及按钮组容器，覆盖常见交互触发场景
- [对话框与窗口控件](org.deepin.dtk/dialogs-and-windows.md) — 窗口与对话框控件涵盖模态/非模态对话框、弹窗、抽屉、应用主窗口、标题栏和关于对话框
- [输入控件](org.deepin.dtk/input-controls.md) — 输入控件涵盖文本编辑、密码、搜索、IP 地址、快捷键、数值微调、复选、单选、开关、下拉选择和滑动条
- [菜单与动作控件](org.deepin.dtk/menus-and-actions.md) — 标准动作和动作组涵盖上下文菜单、菜单栏、菜单项分隔、主题切换菜单以及关于/帮助/退出
- [列表与视图控件](org.deepin.dtk/list-and-views.md) — 列表与导航视图涵盖滚动视图、堆栈视图、滑动视图、列表项代理、排序过滤模型、标签页栏和页面指示器
- [视觉效果与渲染控件](org.deepin.dtk/visual-effects-and-rendering.md) — 视觉效果与渲染控件涵盖阴影、面板、圆角裁剪、高斯模糊、进度指示、动画、标签和提示

