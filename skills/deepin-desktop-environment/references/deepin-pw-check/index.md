# deepin-pw-check

deepin-pw-check 是 DDE 的密码安全策略组件，负责管理系统级密码校验规则。通过 System 总线提供全局密码校验开关、密码长度限制、校验策略、校验规则数量、首字母大写要求的读写及配置管理能力。该接口需要提权操作。

System 总线上的普通策略 getter 不需要客户端统一提权；完整配置读取、覆盖、备份恢复及策略写入由服务端进行授权检查，按对应条目调用。

## D-Bus 接口

### 密码安全策略

提供全局密码安全策略的读写和管理能力，包括密码校验开关、密码长度限制、校验策略、校验规则数量和首字母大写要求。

详见 [org.deepin.dde.PasswdConf1.md](dbus/org.deepin.dde.PasswdConf1.md)
