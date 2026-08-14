# Eval: v20 1070 QML 确认框与 DConfig

## 任务

使用 `$dtk-development` 为 UOS v20 1070 写一个 QML 确认对话框，同时通过 C++
读取 DConfig，并说明该用户配置的缓存位置。

## 期望输出

1. QML 导入 Qt Quick 2.11 与 Qt Quick Controls 2.4，使用 Qt 的 Dialog/Button。
2. 不导入 `org.deepin.dtk`，不使用 D.DTK、DciIcon、ColorSelector 或 DTK QML
   Chameleon。
3. C++ 桥接使用 DConfig 前检查目标 v20 1070 开发包发布的公共头文件，只调用
   其中存在的公开接口，不根据预设的允许或禁止方法清单生成代码。
4. 用户缓存写为
   `{用户家目录}/.config/dsg/configs/{appId}/{subpath}/{configId}.json`。

## 验证要点

- [ ] 使用 Qt Quick/Qt Quick Controls 2
- [ ] 无 DTK QML import、类型、style 或 Declarative 依赖
- [ ] DConfig API 由目标 v20 1070 发布的公共头文件确认
- [ ] 缓存路径符合 v20 1070 daemon
