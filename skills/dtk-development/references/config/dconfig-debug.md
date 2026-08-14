# DConfig 调试

## 版本与服务差异

服务由 `dde-app-services` 提供。v20 常见 daemon 使用默认 dtkcore
缓存布局；v25 的 unit 可能设置 `StateDirectory` 和 cache prefix。以下路径只
用于定位问题，不得写入应用代码；最终以 `systemctl cat/show`、DBus introspection
和 daemon 实际打开的文件为准。

| 项目 | v20 常见值 | v25 常见值 |
|------|------------|------------|
| daemon 用户 | `root` | `deepin-daemon` |
| 用户缓存 | `~/.config/dsg/configs/{appId}/...` | `/var/lib/dde-dconfig-daemon/.config/{uid}/{appId}/...` |
| global 缓存 | `/var/dsg/appdata/configs/{appId}/...` | `/var/lib/dde-dconfig-daemon/.config/global/{appId}/...` |

确认实际状态目录和进程文件：

```bash
systemctl show dde-dconfig-daemon.service -p User -p Environment -p StateDirectory
busctl --system introspect org.desktopspec.ConfigManager /
pid=$(pidof dde-dconfig-daemon)
sudo lsof -p "$pid" | grep -E '/(dsg/configs|dde-dconfig-daemon/.config)/'
```

## 1. 概述与适用场景

DConfig 调试包括服务管理、日志查看、配置文件检查等，用于排查配置相关问题。

**适用场景：**
- 配置不生效问题排查
- 配置服务状态检查
- 配置文件路径确认

**相关工具：**
- `dde-dconfig` CLI 命令
- `dde-dconfig-daemon` 服务
- `DCONFIG_DEBUG` 环境变量

## 2. dde-dconfig-daemon 服务管理

```bash
# 重启服务
sudo systemctl restart dde-dconfig-daemon.service

# 查看日志
sudo journalctl -u dde-dconfig-daemon.service -f -b

# introspection 确认接口支持后，开启详细日志
dbus-send --system --type=method_call --print-reply=literal \
    --dest=org.desktopspec.ConfigManager / \
    org.desktopspec.ConfigManager.enableVerboseLogging

# introspection 确认接口支持后关闭详细日志
dbus-send --system --type=method_call --print-reply=literal \
    --dest=org.desktopspec.ConfigManager / \
    org.desktopspec.ConfigManager.disableVerboseLogging

# v25：确认任务允许影响系统服务后，手动指定用户重启
sudo pkill dde-dconfig-dae && sudo -u deepin-daemon dde-dconfig-daemon

# v25：启动前通过环境变量设置日志
sudo -u deepin-daemon QT_LOGGING_RULES="*dsg.config.debug=true" dde-dconfig-daemon
```

systemd 服务日志通过 journal 查看，文件日志路径由 `LOGS_DIRECTORY` 环境变量控制：`{LOGS_DIRECTORY}/dde-dconfig-daemon/dde-dconfig-daemon.log`。

## 2. 热加载更新

配置描述文件变更后，可通过当前 daemon 暴露的 DBus 接口热加载，无需重启服务。
v20/v25 的方法签名和扫描目录以 introspection 与当前服务实现为准。

### 2.1 全量 reload

```bash
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager / \
    org.desktopspec.ConfigManager.reload
```

实现原理：对比文件签名（大小 + ctime），扫描 `/usr/share/dsg/configs`、`/etc/dsg/configs`、`/var/lib/linglong/entries/share/dsg/configs` 目录，仅对变更文件触发 `update()` 重解析，通过 `valueChanged` 信号通知所有连接。

### 2.2 单文件热更新

```bash
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager / \
    org.desktopspec.ConfigManager.update \
    string:'/usr/share/dsg/configs/<appId>/<configId>.json'
```

### 2.3 同步缓存

```bash
dbus-send --system --type=method_call --print-reply \
    --dest=org.desktopspec.ConfigManager / \
    org.desktopspec.ConfigManager.sync \
    string:'/usr/share/dsg/configs/<appId>/<configId>.json'
```

## 3. 命令行工具

```bash
# 查看应用所有配置
dde-dconfig list -a <appId>

# 列出应用下所有配置子路径
dde-dconfig list -a <appId> -s <subpath>

# 获取配置项
dde-dconfig get -a <appId> -r <configId> -s <subpath> -k <key>

# 设置配置项
dde-dconfig set -a <appId> -r <configId> -s <subpath> -k <key> -v <value>

# 重置配置项
dde-dconfig reset -a <appId> -r <configId> -s <subpath> -k <key>

# 监听配置变化
dde-dconfig watch -a <appId> -r <configId> -s <subpath> -k <key>

# dde-dconfig --help 确认 CLI 支持时：指定用户操作
dde-dconfig get -u <uid> -a <appId> -r <configId> -k <key>

# dde-dconfig --help 确认 CLI 支持时：查询元信息
dde-dconfig get -a <appId> -r <configId> -k <key> -m isDefaultValue

# 启动 GUI 编辑器
dde-dconfig gui
```

GUI 编辑器 `dde-dconfig-editor` 需单独安装：`sudo apt install dde-dconfig-editor`。

## 4. 缓存路径

缓存路径由 dde-dconfig-daemon 中的 `setCachePathPrefix()` 控制。早期版本未显式设置，使用 dtkcore 默认路径；当前版本 daemon 显式指定。

### 4.1 当前路径

| 类型 | 路径 |
|------|------|
| 根路径 | `$STATE_DIRECTORY/.config`（systemd 下为 `/var/lib/dde-dconfig-daemon/.config`） |
| 用户缓存 | `{根路径}/{uid}/{appId}/{configId}.json` |
| global 缓存 | `{根路径}/global/{appId}/{configId}.json` |
| global 降级（全局目录不可写时） | `{根路径}/{appId}-fake-global/{configId}.json` |

### 4.2 路径变更历史

| 版本 | 用户缓存 | global 缓存 |
|------|---------|------------|
| 早期（daemon 未显式设置前缀） | `~/.config/dsg/configs/{appId}/` | `/deepin/appdata/{appId}/configs/` |
| 过渡期 | `~/.config/dsg/configs/{appId}/` | `/var/dsg/appdata/configs/{appId}/` |
| 当前（daemon 显式设置前缀） | `{根路径}/{uid}/{appId}/{configId}.json` | `{根路径}/global/{appId}/{configId}.json` |

> **注意**：版本升级时缓存路径变化可能导致已有缓存失效，配置值回退为 meta 默认值。

## 5. 相关文档

- [concepts.md](concepts.md) - 核心概念
- [dconfig-cpp.md](dconfig-cpp.md) - C++ 方式
- [dconfig-dbus.md](dconfig-dbus.md) - DBus 方式
