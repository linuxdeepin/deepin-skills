---
name: deepin-diskmanager
description: 提供磁盘管理器中的磁盘、分区和硬盘 SMART 信息查询接口
Categories:
  - Application
---

# 磁盘管理器

提供磁盘、分区和硬盘 SMART 信息查询接口。当前 Skill 不暴露无法指定目标的挂载、卸载和服务生命周期控制方法。

授权与目标设备：`getDeviceinfo`/`getalldevice` 可能需要上层授权和磁盘管理器授权前端身份；未授权或调用方身份不匹配时可能返回空结构，不能解释为“没有磁盘”。`getalldevice` 也不保证直接返回可解析列表。SMART 查询的标准链路是先获取设备列表、确定设备路径，再调用对应方法；当前 Skill 不提供设备选择 action。授权前端不可用时应报告环境阻断。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：仅在授权已通过、目标设备已确定且参数有效时返回查询结果；授权失败可能返回空结构，不能当作设备没有数据。
- 需呼出界面并人工操作：无；本 Skill 不提供需要在磁盘管理器窗口继续选择设备的 action。
- 需先启动应用后 D-Bus 才存在：不需要打开磁盘管理器 GUI；裸 D-Bus 调用前需 system 总线上的 `com.deepin.diskmanager` 服务已注册。
- 调用 D-Bus 直接呼出界面：无。

## D-Bus 接口
接口信息：
- Bus：`system`
- Service：`com.deepin.diskmanager`
- Object path：`/com/deepin/diskmanager`
- Interface：`com.deepin.diskmanager`

### get-deviceinfo

获取当前设备信息


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- 无参数。

接口：
- Method：`getDeviceinfo`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=com.deepin.diskmanager /com/deepin/diskmanager com.deepin.diskmanager.getDeviceinfo
```

### getalldevice

获取所有磁盘和分区信息


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- 无参数。

接口：
- Method：`getalldevice`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=com.deepin.diskmanager /com/deepin/diskmanager com.deepin.diskmanager.getalldevice
```

### on-get-device-hard-info

获取硬盘 SMART 硬件信息


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- 无参数。

接口：
- Method：`onGetDeviceHardInfo`


用例：
```bash
dbus-send --system --print-reply --dest=com.deepin.diskmanager /com/deepin/diskmanager com.deepin.diskmanager.onGetDeviceHardInfo
```

### on-get-device-hard-status

获取指定硬盘的健康状态；需要传入设备路径。


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `device`（string）：调用方提供的设备路径，示例占位符 `${DEVICE_PATH}`；调用前需设置为目标硬盘对应的实际设备路径。

接口：
- Method：`onGetDeviceHardStatus`


用例：
```bash
dbus-send --system --print-reply --dest=com.deepin.diskmanager /com/deepin/diskmanager com.deepin.diskmanager.onGetDeviceHardStatus string:"${DEVICE_PATH}"
```
