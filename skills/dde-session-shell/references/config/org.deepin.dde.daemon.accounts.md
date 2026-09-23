# org.deepin.dde.daemon.accounts

账户配置资源，控制快速登录功能的开关。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `enableQuickLogin` | 快速登录开关 | 控制是否启用快速登录功能，开启时开机后自动登录并进入锁屏状态，禁用时无此功能 | bool | readwrite |

## 读写示例

```bash
# 查询快速登录开关
dde-dconfig get -a org.deepin.dde.lightdm-deepin-greeter -r org.deepin.dde.daemon.accounts -k enableQuickLogin
# 设置快速登录开关
dde-dconfig set -a org.deepin.dde.lightdm-deepin-greeter -r org.deepin.dde.daemon.accounts -k enableQuickLogin -v "<value>"
```
