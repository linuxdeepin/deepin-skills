---
name: deepin-deb-installer
description: 提供 Deb 安装器中的安装状态、安装、批量安装和卸载接口；驱动包、架构、签名、依赖和 Deb 有效性检查由设备管理器或系统包管理工具提供
Categories:
  - Application
---

# Deb 包安装器

提供 Deb 包安装状态查询、安装、批量安装和卸载接口

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：`check-install` 返回安装状态；`install`、`uninstall` 在接口返回后完成对应请求。安装和卸载前必须确认目标包及操作；依赖、签名、包信息和 Deb 有效性检查不属于本 Skill 已暴露的能力。
- 需呼出界面并人工操作：`install-batch` 会提交批量安装并打开安装器界面；用户必须在界面确认并完成安装。
- 需先启动应用后 D-Bus 才存在：服务前置：需要 `deepin-deb-installer` 先注册；不要求 Agent 人工打开安装器界面，deepin-tools 可尝试启动安装器。
- 调用 D-Bus 直接呼出界面：`install-batch` 的 `InstallerDeb` 调用会打开批量安装 GUI。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.DebInstaller`
- Object path：`/com/deepin/DebInstaller`
- Interface：`com.deepin.DebInstaller`

### check-install

检查 Deb 包安装状态


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `path`（string）：示例值 `$HOME/Downloads/example.deb`

接口：
- Method：`checkInstallStatus`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.DebInstaller /com/deepin/DebInstaller com.deepin.DebInstaller.checkInstallStatus string:$HOME/Downloads/example.deb
```

### install

安装单个 Deb 包


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `path`（string）：示例值 `$HOME/Downloads/example.deb`

接口：
- Method：`InstallerDebPackge`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.DebInstaller /com/deepin/DebInstaller com.deepin.DebInstaller.InstallerDebPackge string:$HOME/Downloads/example.deb
```

风险警示：
- 会修改系统软件状态和依赖关系；错误的软件包会导致应用不可用，执行前必须确认软件包来源。

### install-batch

批量安装 Deb 包


执行说明：
- 分类：调用 D-Bus 直接呼出界面；后续查看、确认或交互需要人工完成。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `paths`（array of string）：示例值 `$HOME/Downloads/example-a.deb,$HOME/Downloads/example-b.deb`

接口：
- Method：`InstallerDeb`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.DebInstaller /com/deepin/DebInstaller com.deepin.DebInstaller.InstallerDeb array:string:$HOME/Downloads/example-a.deb,$HOME/Downloads/example-b.deb
```

风险警示：
- 会批量修改系统软件状态和依赖关系；错误的软件包会导致应用不可用，执行前必须确认软件包来源。

### uninstall

卸载 Deb 包


执行说明：
- 分类：一步完成；调用返回后取得结果或完成该接口请求。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。

参数：
- `path`（string）：示例值 `example-package`

接口：
- Method：`unInstallDebPackge`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.DebInstaller /com/deepin/DebInstaller com.deepin.DebInstaller.unInstallDebPackge string:example-package
```

风险警示：
- 会卸载软件包并修改系统软件状态；依赖该软件包的应用会影响运行，执行前必须确认软件包名称。
