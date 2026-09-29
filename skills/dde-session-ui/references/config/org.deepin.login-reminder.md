# org.deepin.login-reminder

登录提醒配置资源，控制是否显示登录提醒通知（包括登录信息、密码过期警告和登录失败次数）。

> 范围说明：该配置仅适用于 dde-session-ui 自身的 `deepin-login-reminder` 登录提醒功能，不影响系统中其他组件的登录提醒行为。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `LoginReminder` | 登录提醒 | 控制是否显示登录提醒通知，包括登录信息、密码过期警告和登录失败次数 | bool | readwrite |

## 读写示例

```bash
# 查询登录提醒开关
dde-dconfig get -a org.deepin.login-reminder -r org.deepin.login-reminder -k LoginReminder
# 设置登录提醒开关
dde-dconfig set -a org.deepin.login-reminder -r org.deepin.login-reminder -k LoginReminder -v "<value>"
```
