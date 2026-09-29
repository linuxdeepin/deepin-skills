---
name: deepin-face
description: deepin-face 是 DDE 的人脸识别认证组件，通过 System 总线提供全局的人脸录入、人脸验证、人脸列表查询、人脸重命名、人脸删除、批量删除、默认设备设置、默认服务设置、共享内存信息获取的 D-Bus 接口
Categories:
  - Settings
---

# deepin-face

deepin-face 是 DDE 的人脸识别组件，通过 System 总线提供全局的人脸录入、人脸验证、人脸列表查询、人脸重命名、人脸删除、批量删除、默认设备设置、默认服务设置、共享内存信息获取能力。所有接口面向系统全局用户的人脸数据管理，其中录入、重命名、删除操作需要 polkit 提权。

## D-Bus 接口

### 人脸识别管理

提供全局的人脸录入、人脸验证、人脸列表查询、人脸重命名、人脸删除、批量删除、默认设备设置、默认服务设置、共享内存信息获取能力，面向系统全局用户的人脸数据管理。其中录入、重命名、删除操作需要 polkit 提权。

详见 [org.deepin.dde.Authenticate1.Face.md](references/dbus/org.deepin.dde.Authenticate1.Face.md)
