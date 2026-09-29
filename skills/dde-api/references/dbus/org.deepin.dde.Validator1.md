# org.deepin.dde.Validator1 接口参考

该接口提供主机名和用户名校验能力，用于验证主机名和用户名的合法性。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Validator1` |
| Object path | `/org/deepin/dde/Validator1` |
| Interface | `org.deepin.dde.Validator1` |
| Bus | Session |

## 兼容性说明（废弃）

此执行程序目前没有被使用和编译，该接口为历史遗留接口，无 D-Bus 激活文件，无法通过 D-Bus 自动激活。接口提供 `ValidateHostname` 和 `ValidateUsername` 两个校验方法，保留仅供兼容旧版校验功能参考，不建议在新代码中使用。
