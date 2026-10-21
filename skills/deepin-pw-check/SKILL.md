---
name: deepin-pw-check
description: deepin-pw-check 是 DDE 的密码安全策略组件，通过 System 总线提供密码校验开关、密码长度限制、校验策略、校验规则数量、首字母大写要求的系统级读写及配置管理接口，提供密码校验 C 接口开发库
Categories:
  - Settings
  - Develop
---

# deepin-pw-check

deepin-pw-check 是 DDE 的密码安全策略组件，负责管理系统级密码校验规则。通过 System 总线提供全局密码校验开关、密码长度限制、校验策略、校验规则数量、首字母大写要求的读写及配置管理能力。该接口需要提权操作。

System 总线上的普通策略 getter 不需要客户端统一提权；完整配置读取、覆盖、备份恢复及策略写入由服务端进行授权检查，按对应条目调用。C 库只用于程序中的密码校验，与修改系统密码策略分开。

## D-Bus 接口

### 密码安全策略

提供全局密码安全策略的读写和管理能力，包括密码校验开关、密码长度限制、校验策略、校验规则数量和首字母大写要求。

详见 [org.deepin.dde.PasswdConf1.md](references/dbus/org.deepin.dde.PasswdConf1.md)

## 开发接口

deepin-pw-check 是 DDE 密码强度校验 C 语言库，提供密码复杂度校验、密码强度等级评估、密码校验策略查询、错误码到可读信息转换和调试日志控制能力。使用方在 C 或 C++ 程序中链接该库即可调用相关接口。

### 密码校验接口

C 接口参考文档，以公开头文件 `deepin_pw_check.h` 为入口，涵盖密码复杂度校验、密码强度等级评估、密码校验策略查询、错误码到可读信息转换和调试控制能力的全部公开接口。

详见 [password-check.md](references/interface/password-check.md)
