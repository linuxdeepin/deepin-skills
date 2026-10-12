# org.deepin.dde.daemon.accounts

账户配置资源，来自 dde-daemon 仓库，注册在 appId `org.deepin.dde.lightdm-deepin-greeter` 下，控制快速登录功能的开关。

## 配置项

| Key | Name | Description | 类型 | Permissions | Visibility |
|---|---|---|---|---|---|
| `enableQuickLogin` | 启用快速登录 | 是否启用快速登录，开启配置时，开机后自动登录并进入锁屏状态；禁用配置时，无此功能。 | bool | readwrite | public |

## 读写示例

```bash
# 查询快速登录开关
dde-dconfig get -a org.deepin.dde.lightdm-deepin-greeter -r org.deepin.dde.daemon.accounts -k enableQuickLogin
# 开启快速登录
dde-dconfig set -a org.deepin.dde.lightdm-deepin-greeter -r org.deepin.dde.daemon.accounts -k enableQuickLogin -v true
# 关闭快速登录
dde-dconfig set -a org.deepin.dde.lightdm-deepin-greeter -r org.deepin.dde.daemon.accounts -k enableQuickLogin -v false
```
