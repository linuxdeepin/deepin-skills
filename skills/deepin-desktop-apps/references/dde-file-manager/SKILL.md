---
name: dde-file-manager
description: 提供文件管理器中的块设备、协议设备安全弹出、保险箱、最近文件、操作撤销重做和全文索引接口
Categories:
  - Application
---

# 文件管理器

提供块设备、协议设备安全弹出、保险箱、最近文件、操作撤销重做和全文索引接口；不提供复制、移动和删除文件接口。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：所有已提供的设备、保险箱、最近文件、撤销/重做和全文索引 action 都在一次 D-Bus 调用后返回结果或完成请求；弹出、锁定和清空等有副作用的 action 仍须先确认目标。
- 需呼出界面并人工操作：无；本 Skill 不提供需要在文件管理器窗口继续操作的 action。
- 需先启动应用后 D-Bus 才存在：不需要人工打开文件管理器窗口；裸 D-Bus 调用只要求对应文件管理器守护进程服务已注册，源工具不负责自动启动该守护进程。
- 调用 D-Bus 直接呼出界面：无。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`org.deepin.Filemanager.Daemon`
- Object path：`/org/deepin/Filemanager/Daemon/DeviceManager`
- Interface：`org.deepin.Filemanager.Daemon.DeviceManager`

### block-devices

列出块设备 ID


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `mode`（int32）：示例值 `0`

接口：
- Method：`GetBlockDevicesIdList`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/DeviceManager org.deepin.Filemanager.Daemon.DeviceManager.GetBlockDevicesIdList int32:0
```

### block-info

查询块设备详情


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `id`（string）：示例值 `sda1`
- `include_children`（boolean）：示例值 `false`

接口：
- Method：`QueryBlockDeviceInfo`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/DeviceManager org.deepin.Filemanager.Daemon.DeviceManager.QueryBlockDeviceInfo string:sda1 boolean:false
```

### protocol-devices

列出协议设备 ID


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`GetProtocolDevicesIdList`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/DeviceManager org.deepin.Filemanager.Daemon.DeviceManager.GetProtocolDevicesIdList
```

### protocol-info

查询协议设备详情


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `id`（string）：示例值 `mtp-001`
- `include_children`（boolean）：示例值 `false`

接口：
- Method：`QueryProtocolDeviceInfo`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/DeviceManager org.deepin.Filemanager.Daemon.DeviceManager.QueryProtocolDeviceInfo string:mtp-001 boolean:false
```

### monitor-status

查询设备监控状态


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`IsMonotorWorking`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/DeviceManager org.deepin.Filemanager.Daemon.DeviceManager.IsMonotorWorking
```

### eject-block

安全弹出块设备


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `id`（string）：示例值 `sda1`

接口：
- Method：`DetachBlockDevice`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/DeviceManager org.deepin.Filemanager.Daemon.DeviceManager.DetachBlockDevice string:sda1
```

风险警示：
- 会卸载指定块设备，设备上的未保存写入会中断；执行前必须确认没有程序正在使用目标设备。

### eject-protocol

安全弹出协议设备


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `id`（string）：示例值 `mtp-001`

接口：
- Method：`DetachProtocolDevice`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/DeviceManager org.deepin.Filemanager.Daemon.DeviceManager.DetachProtocolDevice string:mtp-001
```

风险警示：
- 会卸载指定协议设备，设备上的未保存写入会中断；执行前必须确认没有程序正在使用目标设备。

### eject-all

弹出所有已挂载设备


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`DetachAllMountedDevices`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/DeviceManager org.deepin.Filemanager.Daemon.DeviceManager.DetachAllMountedDevices
```

风险警示：
- 会卸载全部已挂载设备，设备上的未保存写入会中断；执行前必须确认没有程序正在使用目标设备。

接口信息：
- Bus：`session`
- Service：`org.deepin.Filemanager.Daemon`
- Object path：`/org/deepin/Filemanager/Daemon/VaultManager`
- Interface：`org.deepin.Filemanager.Daemon.VaultManager`

### vault-locked

查询保险箱锁定状态


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`IsLockEventTriggered`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/VaultManager org.deepin.Filemanager.Daemon.VaultManager.IsLockEventTriggered
```

### vault-lock

锁定保险箱


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`TriggerLockEvent`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/VaultManager org.deepin.Filemanager.Daemon.VaultManager.TriggerLockEvent
```

### vault-wait-minutes

查询保险箱密码锁定延迟分钟数


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`GetNeedWaitMinutes`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/VaultManager org.deepin.Filemanager.Daemon.VaultManager.GetNeedWaitMinutes
```

接口信息：
- Bus：`session`
- Service：`org.deepin.Filemanager.Daemon`
- Object path：`/org/deepin/Filemanager/Daemon/RecentManager`
- Interface：`org.deepin.Filemanager.Daemon.RecentManager`

### recent-paths

获取最近文件路径列表


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`GetItemsPath`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/RecentManager org.deepin.Filemanager.Daemon.RecentManager.GetItemsPath
```

### recent-info

获取最近文件详细信息


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`GetItemsInfo`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/RecentManager org.deepin.Filemanager.Daemon.RecentManager.GetItemsInfo
```

### recent-reload

重新加载最近文件记录，会刷新当前最近文件列表。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`Reload`

用例：
```bash
dbus-send --session --print-reply \
  --dest=org.deepin.Filemanager.Daemon \
  /org/deepin/Filemanager/Daemon/RecentManager \
  org.deepin.Filemanager.Daemon.RecentManager.Reload
```

### recent-purge

清空最近文件记录


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`PurgeItems`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/RecentManager org.deepin.Filemanager.Daemon.RecentManager.PurgeItems
```

接口信息：
- Bus：`session`
- Service：`org.deepin.Filemanager.Daemon`
- Object path：`/org/deepin/Filemanager/Daemon/OperationsStackManager`
- Interface：`org.deepin.Filemanager.Daemon.OperationsStackManager`

### undo

撤销上一个文件操作


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`RevocationOperations`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/OperationsStackManager org.deepin.Filemanager.Daemon.OperationsStackManager.RevocationOperations
```

### redo

重做上一个撤销操作


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`RevocationRedoOperations`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.Daemon /org/deepin/Filemanager/Daemon/OperationsStackManager org.deepin.Filemanager.Daemon.OperationsStackManager.RevocationRedoOperations
```

接口信息：
- Bus：`session`
- Service：`org.deepin.Filemanager.TextIndex`
- Object path：`/org/deepin/Filemanager/TextIndex`
- Interface：`org.deepin.Filemanager.TextIndex`

### index-enable

查询或设置全文索引开关。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `enabled`（boolean）（可选）：设置为 `true` 启用，设置为 `false` 禁用；省略时查询当前状态。

接口：
- Methods：`IsEnabled`（查询）、`SetEnabled`（设置）

用例：IsEnabled
```bash
dbus-send --session --print-reply \
  --dest=org.deepin.Filemanager.TextIndex \
  /org/deepin/Filemanager/TextIndex \
  org.deepin.Filemanager.TextIndex.IsEnabled
```

用例：SetEnabled
```bash
dbus-send --session --print-reply \
  --dest=org.deepin.Filemanager.TextIndex \
  /org/deepin/Filemanager/TextIndex \
  org.deepin.Filemanager.TextIndex.SetEnabled \
  boolean:true
```

### index-status

查询索引任务是否运行


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`HasRunningTask`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.TextIndex /org/deepin/Filemanager/TextIndex org.deepin.Filemanager.TextIndex.HasRunningTask
```

### index-exists

查询索引数据库是否存在


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`IndexDatabaseExists`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.TextIndex /org/deepin/Filemanager/TextIndex org.deepin.Filemanager.TextIndex.IndexDatabaseExists
```

### index-last-update

查询索引最后更新时间


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`GetLastUpdateTime`

用例：
```bash
dbus-send --session --print-reply --dest=org.deepin.Filemanager.TextIndex /org/deepin/Filemanager/TextIndex org.deepin.Filemanager.TextIndex.GetLastUpdateTime
```
