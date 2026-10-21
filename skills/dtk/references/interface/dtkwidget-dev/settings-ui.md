# 设置界面

提供从配置模型自动生成设置界面的框架，通过设置对话框和控件工厂将配置项映射为复选框、下拉框两类界面控件。

## DSettingsDialog

### 定位

DTK 设置对话框。

### 功能能力总结

基于 DSettings 配置框架构建设置界面，支持分组、分页展示设置项。通过 DSettingsWidgetFactory 创建各设置项的编辑控件。

### 使用场景

需要为应用程序设置界面时；使用 DTK 设置框架管理应用配置时。


---

## DSettingsWidgetFactory

### 定位

DTK 设置控件工厂。

### 功能能力总结

根据设置项类型和自定义键值创建对应的编辑控件，支持注册自定义控件创建函数。与 DSettingsDialog 配合使用，将设置项映射为具体的编辑控件。

### 使用场景

需要自定义设置界面中的控件类型时；需要为设置项创建自定义编辑控件时。


---

## 最小使用示例

链接 `Dtk6::Widget`，并在已创建 DApplication 的 GUI 线程调用；参考库入口的集成说明。从调用方提供的 DSettings 模型构建界面。模型应先按公开 JSON 格式创建，并由调用方保持存活。

```cpp
#include <DSettings>
#include <DSettingsDialog>

void showSettings(Dtk::Core::DSettings *settings, QWidget *parent)
{
    auto *dialog = new Dtk::Widget::DSettingsDialog(parent);
    dialog->setAttribute(Qt::WA_DeleteOnClose);
    dialog->updateSettings(settings);
    dialog->open();
}
```
