# Eval: 显式目标覆盖宿主环境

## 任务

当前开发机是 UOS v25，用户明确要求修复运行在 UOS v20 1070 上的 DTK5 应用，
其中有一个 QML 确认页。请确定兼容基线和 QML 技术选择。

## 期望输出

1. 采用用户指定的 v20 1070，不让当前 v25 宿主覆盖目标。
2. 使用 Qt 5.11/DTK5；DTK C++ 固定按 1070 API。
3. QML 只使用 Qt Quick/Qt Quick Controls 2，不使用 dtkdeclarative、
   `org.deepin.dtk`、D.DTK 或 DTK QML Chameleon。

## 验证要点

- [ ] 目标为 v20 1070
- [ ] 区分目标系统与当前宿主系统
- [ ] QML 使用 Qt 提供的模块
- [ ] 没有 DTK QML import、类型或依赖
