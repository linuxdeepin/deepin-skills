# org.deepin.ds.launchpad

启动器应用配置资源，控制 dde-launchpad 的按桌面条目 ID 搜索行为。该配置资源挂载在 appId `org.deepin.dde.shell` 下（dde-launchpad 以 dde-shell applet 形式运行），仅作用于 dde-launchpad 自身应用行为，不影响系统全局配置。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `searchByDesktopId` | 按桌面条目 ID 搜索 | 搜索时是否允许按桌面条目 ID 进行搜索 | bool | readwrite |

## 读写示例

```bash
# 查询是否按桌面条目 ID 搜索
dde-dconfig get -a org.deepin.dde.shell -r org.deepin.ds.launchpad -k searchByDesktopId
# 设置是否按桌面条目 ID 搜索
dde-dconfig set -a org.deepin.dde.shell -r org.deepin.ds.launchpad -k searchByDesktopId -v true
```
