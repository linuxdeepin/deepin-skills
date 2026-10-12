# org.deepin.dde.am.appoverride

应用属性会话级覆盖资源，用于在会话级别覆盖应用的 Exec、TryExec 和 Icon 字段，使应用管理器在启动应用时使用覆盖后的值而非桌面文件中的原始值。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `Exec` | Exec 覆盖 | 会话级覆盖桌面文件的 Exec 字段，支持 `!AM_FULL!` 占位符（占位符会被替换为应用管理器的完整路径） | string | readonly |
| `TryExec` | TryExec 覆盖 | 会话级覆盖桌面文件的 TryExec 字段，空字符串时强制显示该应用（即跳过 TryExec 检查） | string | readonly |
| `Icon` | Icon 覆盖 | 会话级覆盖桌面文件的 Icon 字段 | string | readwrite |

## 读写示例

```bash
# 查询 Exec 覆盖
dde-dconfig get -a org.deepin.dde.application-manager -r org.deepin.dde.am.appoverride -k Exec
# 查询 TryExec 覆盖
dde-dconfig get -a org.deepin.dde.application-manager -r org.deepin.dde.am.appoverride -k TryExec
# 查询 Icon 覆盖
dde-dconfig get -a org.deepin.dde.application-manager -r org.deepin.dde.am.appoverride -k Icon
# 设置 Icon 覆盖（string 类型）
dde-dconfig set -a org.deepin.dde.application-manager -r org.deepin.dde.am.appoverride -k Icon -v "my-custom-icon"
```
