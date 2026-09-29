# org.deepin.dde.control-center.commoninfo

通用信息配置资源，控制只读保护显示、开机壁纸编辑和 GRUB 用户名显示配置。

## 配置项

| Key | Name | Description | 类型 | 取值范围 | Permissions | Flags |
|---|---|---|---|---|---|---|
| `showReadOnlyProtection` | 只读保护显示开关 | 控制是否在开发者模式中显示只读保护选项 | bool | true / false | readwrite | |
| `bootWallpaperEnabled` | 开机壁纸编辑开关 | 控制 GRUB "boot menu" 壁纸是否可编辑 | bool | true / false | readwrite | |
| `bootGrubUserNameVisible` | GRUB 用户名显示开关 | 控制"启动菜单验证"的验证密码弹窗中是否显示用户名 | bool | true / false | readwrite | |

## 读写示例

```bash
# 查询只读保护显示开关
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center.commoninfo -k showReadOnlyProtection
# 设置只读保护显示开关
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center.commoninfo -k showReadOnlyProtection -v "<value>"

# 查询开机壁纸编辑开关
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center.commoninfo -k bootWallpaperEnabled
# 设置开机壁纸编辑开关
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center.commoninfo -k bootWallpaperEnabled -v "<value>"

# 查询 GRUB 用户名显示开关
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center.commoninfo -k bootGrubUserNameVisible
# 设置 GRUB 用户名显示开关
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center.commoninfo -k bootGrubUserNameVisible -v "<value>"
```
