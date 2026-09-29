# dde-fakewm 命令参考

DDE 虚拟窗口管理器，是 dde-appearance 项目自身的开发/调试工具。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-appearance` |
| 安装路径 | `/usr/bin/dde-fakewm` |
| DDE 角色 | 外观模块开发/调试用的虚拟窗口管理器 |

## 用途

DDE 虚拟窗口管理器，是 dde-appearance 项目自身的开发/调试工具。它模拟一个最小化的窗口管理器环境，用于测试外观相关功能（如主题切换和窗口装饰）在无完整窗口管理器时的行为。

该工具不使用 QCommandLineParser，不接受命令行参数，主要用于开发调试。它会在 Session 总线上注册 `com.deepin.wm` D-Bus 服务，以便在没有真实窗口管理器时模拟相关接口。

> **注意**：该工具仅支持 X11 会话，在 Wayland 会话下会直接退出。

## 使用方式

### 通过 systemd 服务启动

dde-fakewm 通常通过 systemd 用户服务启动：

```bash
systemctl --user start dde-fakewm.service
```

查看服务状态：

```bash
systemctl --user status dde-fakewm.service
```

停止服务：

```bash
systemctl --user stop dde-fakewm.service
```

### 直接运行

二进制位于 `/usr/bin/dde-fakewm`，在默认 PATH 中，可直接执行（需在 X11 会话环境下）：

```bash
dde-fakewm
```

启动后可通过以下命令验证 D-Bus 服务是否已注册：

```bash
gdbus call --session \
  --dest org.freedesktop.DBus \
  --object-path /org/freedesktop/DBus \
  --method org.freedesktop.DBus.ListNames | grep com.deepin.wm
```
