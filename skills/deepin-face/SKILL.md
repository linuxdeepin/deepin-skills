---
name: deepin-face
description: 通过 System 总线管理指定用户的人脸录入、验证、列表、重命名与删除，提供认证设备和服务默认项、共享内存信息查询。新接口由 deepin-authenticate 包的 org.deepin.dde.Authenticate1 服务提供；旧版 Face1 不提供全部新能力。
Categories:
  - Settings
---

# deepin-face

deepin-face 是 DDE 的人脸识别组件，通过 System 总线管理指定用户的人脸录入、验证、查询、重命名与删除，另提供认证设备/服务默认项及共享内存信息。人脸操作按参数指定用户和模板；设备默认项作用于指定服务，默认服务设置作用于认证服务。录入、重命名和删除按对应条目取得授权；验证启动、人脸列表和默认设备/服务设置另有 root 调用限制，不能以普通查询示例代替。

新接口由 `deepin-authenticate` 包提供，调用前需确保 System 总线上的 `org.deepin.dde.Authenticate1` 服务可用；旧版独立人脸组件的 `Face1` 接口不包含新服务的全部能力。按条目传入目标用户和人脸标识，不能将单个人脸操作理解为修改所有用户。

## D-Bus 接口

### 人脸识别管理

按用户名、服务名与模板标识执行人脸操作，并提供默认认证设备/服务与共享内存查询；权限和影响范围见对应方法。

详见 [org.deepin.dde.Authenticate1.Face.md](references/dbus/org.deepin.dde.Authenticate1.Face.md)
