# Chameleon 风格机制

## 任务

分别处理一个 QWidget 风格问题和一个 v25 QML 风格问题，要求：
1. 先判定当前 UI 技术栈，只加载对应的 Chameleon 专篇
2. 说明控件如何获取状态颜色
3. 说明调色板如何影响控件外观
4. 需要比较两套实现时按目标系统能力读取两个专篇

## 验证要点

- [ ] 理解 ChameleonStyle 是 QStyle 插件
- [ ] 理解 DStyleHelper 状态颜色计算
- [ ] 理解 DPalette 与 Chameleon 的关系
- [ ] QWidget 任务读取 `chameleon-widget.md`，不加载 QML 专篇
- [ ] v25 QML 任务读取 `chameleon-qml.md`，不加载 QWidget 专篇
- [ ] 跨栈比较直接读取两个专篇，不依赖额外总览文档
- [ ] 明确 QML Chameleon 仅适用于 v25；v20 QML 使用 Qt style
