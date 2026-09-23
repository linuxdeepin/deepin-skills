# org.deepin.ds.launchpad

启动器配置资源，控制启动器搜索时是否允许按桌面条目 ID 进行搜索。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `searchByDesktopId` | 按桌面 ID 搜索 | 控制启动器搜索时是否允许按桌面条目 ID 进行搜索 | bool | readwrite |

## 读写示例

```bash
# 查询是否按桌面 ID 搜索
dde-dconfig get -a org.deepin.dde.shell -r org.deepin.ds.launchpad -k searchByDesktopId
# 设置是否按桌面 ID 搜索
dde-dconfig set -a org.deepin.dde.shell -r org.deepin.ds.launchpad -k searchByDesktopId -v "<value>"
```

## 覆盖说明

- 该资源存在 Override 覆盖：`excludeAppIdList` 被 `org.deepin.dde.shell/org.deepin.ds.launchpad/3000-org.deepin.ds.launchpad.override.json` 覆盖

此外，dde-shell 还存在以下资源的 Override 覆盖（这些资源不在公开配置中，仅记录覆盖关系）：

- `org.deepin.ds.dock`：`Item_Alignment` 被 `org.deepin.dde.shell/org.deepin.ds.dock/3000-org.deepin.ds.dock.override.json` 覆盖
- `org.deepin.ds.dock.taskmanager`：`Docked_Items` 被 `org.deepin.dde.shell/org.deepin.ds.dock.taskmanager/3000-org.deepin.ds.dock.taskmanager.override.json` 覆盖
