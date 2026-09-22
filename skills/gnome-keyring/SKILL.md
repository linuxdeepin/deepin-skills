---
name: gnome-keyring
description: 提供 Secret Service API 密钥库服务和 GNOME 密钥环守护进程接口（上游 GNOME 项目）
Categories:
  - Application
---

# gnome-keyring

gnome-keyring 是上游 GNOME 项目的密钥环管理组件，通过 Session 总线提供 Secret Service API 密钥库服务和 GNOME 密钥环守护进程接口。该接口来源于上游 GNOME 项目。

## D-Bus 接口

### 密钥库服务

提供 Secret Service API 的会话管理、集合创建、密钥搜索、锁定解锁能力。

详见 [org.freedesktop.Secret.Service.md](references/dbus/org.freedesktop.Secret.Service.md)

### 密钥环守护进程

提供 GNOME 密钥环守护进程控制能力。

详见 [org.gnome.keyring.Daemon.md](references/dbus/org.gnome.keyring.Daemon.md)

