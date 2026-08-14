# Eval: 未指定目标时判断系统版本

## 任务

用户没有说明目标系统版本，当前系统 `/etc/os-version` 的 `[Version]` 节包含
`MajorVersion=25`、`MinorVersion=2500`。请说明本次 DTK 开发应采用哪个系统版本
基线，以及下一步还要确认什么。

## 期望输出

1. 按 `DSysInfo::majorVersion()`/`minorVersion()` 的实现判断为 v25。
2. 使用 `/etc/os-version` 的 `[Version]` 节，不以 `/etc/os-release` 的
   `VERSION_ID` 替代。
3. 随后独立检查目标工程的 Qt/DTK ABI、QWidget/QML 与构建系统。

## 验证要点

- [ ] 选择 v25，并记录 `MinorVersion=2500`
- [ ] 提到 `DSysInfo` 与 `/etc/os-version`
- [ ] 没有把 `MinorVersion=2500` 写成 v25 的固定支持版本
- [ ] 没有把 v25 自动等同于 DTK6
- [ ] 检查目标工程的 DTK5/DTK6 与构建方式
