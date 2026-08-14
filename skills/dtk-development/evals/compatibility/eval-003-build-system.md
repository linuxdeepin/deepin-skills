# Eval: v20 构建系统选择

## 任务

用户明确要求在 v20 环境分别修改一个使用顶层 `CMakeLists.txt` 的 DTK 核心项目，以及一个使用顶层 `.pro` 文件的 Qt 平台集成项目。请给出本地 Debug 构建策略。

## 期望输出

回答应：

1. 对 CMake 工程使用 Qt5/DTK5 的普通 CMake 构建，不套用 v25 的 `DTK5=ON/OFF` 双 ABI 规则。
2. 对 `.pro` 工程使用目标 Qt 5 qmake，并先确认 qmake 的 Qt 版本、头文件路径和私有依赖。
3. 以工程真实构建文件和 option 为准，不通过构建系统反推目标系统版本。
4. 明确 v20 不使用 DTK5/DTK6 Build Profile，也不存在 `DTK5` CMake option；
   `nodtk5`/`nodtk6` 和 `-DDTK5=ON/OFF` 仅用于 v25。

## 验证要点

- [ ] CMake 命令包含独立 build 目录和 Debug 配置
- [ ] qmake 命令包含 `CONFIG+=debug`
- [ ] 提到 Qt 5.11 兼容工具链或匹配目标 Qt5 工具链
- [ ] 没有对 v20 工程无条件添加 `-DDTK5=ON`
- [ ] 没有对 v20 使用 `nodtk5` 或 `nodtk6` Build Profile
