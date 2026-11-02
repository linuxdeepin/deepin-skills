---
name: deepin-devicemanager
description: 提供系统硬件设备的信息查询、状态检查、GPU 查询、可移除设备查询、驱动包检查和 Deb 包检查接口；不负责系统版本信息或 CPU、内存、进程运行时资源占用查询
Categories:
  - Application
---

# 设备管理器

提供系统硬件设备的信息查询、状态检查、GPU 查询、可移除设备查询、驱动包检查和 Deb 包检查接口。不负责系统版本信息或 CPU、内存、进程运行时资源占用查询。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：免授权的硬件查询返回结果；需要设备控制或包校验授权的接口在授权通过后返回结果，授权失败或返回空结构时必须报告授权状态。`refresh` 返回表示刷新请求已提交。
- 需呼出界面并人工操作：无。
- 需先启动应用后 D-Bus 才存在：不需要打开设备管理器 GUI；裸 D-Bus 调用只要求 system 总线上的 `org.deepin.DeviceInfo`/`org.deepin.DeviceControl` 服务可用。
- 调用 D-Bus 直接呼出界面：无。

## D-Bus 接口
接口信息：
- Bus：`system`
- Service：`org.deepin.DeviceInfo`
- Object path：`/org/deepin/DeviceInfo`
- Interface：`org.deepin.DeviceInfo`

### info

查询设备信息


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `key`（string）：示例值 `cpu`

接口：
- Method：`getInfo`


说明：`lscpu`/`lscpu_num` 等只读 CPU 查询可按普通用户路径尝试；其他需要设备控制或包校验权限的 key/action 仍需上层授权。

用例：
```bash
dbus-send --system --print-reply --dest=org.deepin.DeviceInfo /org/deepin/DeviceInfo org.deepin.DeviceInfo.getInfo string:lscpu
```

### refresh

刷新设备信息缓存


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- 无参数。

接口：
- Method：`refreshInfo`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=org.deepin.DeviceInfo /org/deepin/DeviceInfo org.deepin.DeviceInfo.refreshInfo
```

### gpu-info

获取 GPU 详细信息


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- 无参数。

接口：
- Method：`getGpuInfoForFTDTM`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=org.deepin.DeviceInfo /org/deepin/DeviceInfo org.deepin.DeviceInfo.getGpuInfoForFTDTM
```

接口信息：
- Bus：`system`
- Service：`org.deepin.DeviceControl`
- Object path：`/org/deepin/DeviceControl`
- Interface：`org.deepin.DeviceControl`

### removable

获取可移除设备列表


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- 无参数。

接口：
- Method：`getRemoveInfo`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=org.deepin.DeviceControl /org/deepin/DeviceControl org.deepin.DeviceControl.getRemoveInfo
```

### disabled

获取被禁用设备列表


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- 无参数。

接口：
- Method：`getAuthorizedInfo`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=org.deepin.DeviceControl /org/deepin/DeviceControl org.deepin.DeviceControl.getAuthorizedInfo
```

### is-enabled

查询设备是否启用


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- `unique_id`（string）：示例值 `pci-0000:00:02.0`

接口：
- Method：`isDeviceEnabled`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=org.deepin.DeviceControl /org/deepin/DeviceControl org.deepin.DeviceControl.isDeviceEnabled string:pci-0000:00:02.0
```

### is-network-wakeup

查询网卡网络唤醒是否启用


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- `name`（string）：示例值 `eth0`

接口：
- Method：`isNetworkWakeup`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=org.deepin.DeviceControl /org/deepin/DeviceControl org.deepin.DeviceControl.isNetworkWakeup string:eth0
```

### is-driver-pkg

检查 Deb 包是否为驱动包


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- `path`（string）：示例值 `$HOME/Downloads/driver.deb`

接口：
- Method：`isDriverPackage`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=org.deepin.DeviceControl /org/deepin/DeviceControl org.deepin.DeviceControl.isDriverPackage string:$HOME/Downloads/driver.deb
```

### is-blacklisted

检查驱动模块是否在黑名单


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- `module`（string）：示例值 `nouveau`

接口：
- Method：`isBlackListed`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=org.deepin.DeviceControl /org/deepin/DeviceControl org.deepin.DeviceControl.isBlackListed string:nouveau
```

### is-arch-matched

检查 Deb 包架构是否匹配


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- `path`（string）：示例值 `$HOME/Downloads/driver.deb`

接口：
- Method：`isArchMatched`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=org.deepin.DeviceControl /org/deepin/DeviceControl org.deepin.DeviceControl.isArchMatched string:$HOME/Downloads/driver.deb
```

### is-deb-valid

检查 Deb 包是否有效


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 授权：该条目声明了 `requires_sudo: true`，按上层权限流程处理。

参数：
- `path`（string）：示例值 `$HOME/Downloads/driver.deb`

接口：
- Method：`isDebValid`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=org.deepin.DeviceControl /org/deepin/DeviceControl org.deepin.DeviceControl.isDebValid string:$HOME/Downloads/driver.deb
```
