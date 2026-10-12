# org.deepin.dtk.settings QML 模块

org.deepin.dtk.settings 是 dtkdeclarative 提供的设置界面 QML 模块，为 DTK 应用提供开箱即用的设置对话框框架。模块内置导航栏与内容区的联动布局，支持从配置模型自动生成复选框、下拉框、文本输入三类配置项控件，统一遵循 DTK 主题样式。

## 集成

### 使用方式

QML 模块 URI 为 `org.deepin.dtk.settings`，导入版本为 1.0。模块以动态插件形式发布，使用方无需安装额外模块包，确保系统已安装 dtkdeclarative 运行时库即可。

在 QML 文件中导入：

```qml
import org.deepin.dtk.settings 1.0
```

导入后可使用模块中的所有设置控件类型。

## 模块API介绍

### CheckBox

#### 定位

继承 Settings.OptionDelegate 的 DTK 控件。

#### 功能能力总结

以复选框形式展示和编辑布尔型配置项，自动与配置选项双向同步：勾选状态实时回写配置值，配置值变更时自动更新勾选状态。

#### 使用场景

需要使用 DTK 主题样式的 settings/CheckBox 控件时使用。

### ComboBox

#### 定位

继承 Settings.OptionDelegate 的 DTK 控件。

#### 功能能力总结

以下拉列表形式展示和编辑枚举型配置项，支持通过数据角色匹配当前选中项，选择变更时自动将选中值回写配置选项。

#### 使用场景

需要使用 DTK 主题样式的 settings/ComboBox 控件时使用。

### ContentBackground

#### 定位

继承 Rectangle 的 DTK 控件。

#### 功能能力总结

为设置内容区域提供带圆角的背景容器，根据分组层级自动调整左右边距，保持不同层级内容的视觉缩进一致性。

#### 使用场景

需要使用 DTK 主题样式的 settings/ContentBackground 控件时使用。

### ContentTitle

#### 定位

继承 Label 的 DTK 控件。

#### 功能能力总结

显示设置分组的标题文字，根据分组层级自动调整字体大小和边距，为设置内容提供层级化的视觉标识。

#### 使用场景

需要使用 DTK 主题样式的 settings/ContentTitle 控件时使用。

### LineEdit

#### 定位

继承 Settings.OptionDelegate 的 DTK 控件。

#### 功能能力总结

以单行文本输入框形式展示和编辑字符串型配置项，编辑完成后自动将输入文本回写配置选项。

#### 使用场景

需要使用 DTK 主题样式的 settings/LineEdit 控件时使用。

### NavigationTitle

#### 定位

继承 Control 的 DTK 控件。

#### 功能能力总结

在设置对话框导航栏中显示分组标题，支持点击切换当前选中分组，选中状态时高亮显示以指示当前所在位置。

#### 使用场景

需要使用 DTK 主题样式的 settings/NavigationTitle 控件时使用。

### OptionDelegate

#### 定位

继承 RowLayout 的 DTK 控件。

#### 功能能力总结

作为设置项的通用行布局基类，在左侧显示配置项名称标签，支持控制名称标签的显示与隐藏，为各类设置控件提供统一的布局结构。

#### 使用场景

需要使用 DTK 主题样式的 settings/OptionDelegate 控件时使用。

### SettingsDialog

#### 定位

继承 DialogWindow 的 DTK 控件。

#### 功能能力总结

提供设置对话框的主窗口框架，左侧导航栏列出所有设置分组并支持点击切换，右侧内容区域同步展示对应分组的设置项，底部提供恢复默认值按钮，导航与内容区域双向联动。

#### 使用场景

需要使用 DTK 主题样式的 settings/SettingsDialog 控件时使用。

### Style

#### 定位

继承 FlowStyle 的 DTK 控件。

#### 功能能力总结

作为设置模块的样式单例，继承全局流式样式参数，为设置对话框中的导航栏、内容区域、标题组件提供统一的边距、宽度、高度、文本垂直内边距和重置按钮高度样式参数。

#### 使用场景

需要使用 DTK 主题样式的 style/Style 控件时使用。
