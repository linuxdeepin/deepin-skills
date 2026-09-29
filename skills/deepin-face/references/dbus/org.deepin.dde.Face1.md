# org.deepin.dde.Face1 接口参考（兼容接口）

## 功能概述

`org.deepin.dde.Face1` 是旧版 `deepin-face` 独立组件提供的 D-Bus 接口（对象路径 `/org/deepin/dde/Face1`，System 总线），提供以下基础人脸识别功能：

- **人脸录入**：EnrollStart / EnrollStop
- **人脸验证**：VerifyStart / VerifyStop
- **人脸删除**：Delete
- **属性**：Claim（设备占用状态）、List（人脸列表）、CharaType（特征类型）
- **信号**：ErollStatus（录入状态）、VerifyStatus（验证状态）

## 接口关系

`org.deepin.dde.Face1` 与 `org.deepin.dde.Authenticate1.Face` 是**废弃关系**：

- `org.deepin.dde.Face1` 来自旧版 `deepin-face` 独立组件，仅提供基础的人脸录入、验证、删除功能，已废弃，不应在新代码中使用。
- `org.deepin.dde.Authenticate1.Face` 来自 `deepin-authentication` 统一认证服务，后者提供了更完整的人脸管理能力（包括人脸重命名、批量删除、默认设备设置、默认服务设置、共享内存信息获取、设备状态信号、属性查询）。

**新代码应使用 `org.deepin.dde.Authenticate1.Face` 接口。**

---
