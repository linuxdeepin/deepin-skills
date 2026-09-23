# org.deepin.dde.control-center.accounts

账户头像配置资源，管理控制中心账户管理中当前用户的头像图片路径。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `avatarPath` | 用户头像路径 | 配置控制中心账户管理中当前用户的头像图片路径 | string | readwrite |

## 读写示例

```bash
# 查询头像路径
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center.accounts -k avatarPath
# 设置头像路径
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center.accounts -k avatarPath -v "<value>"
```
