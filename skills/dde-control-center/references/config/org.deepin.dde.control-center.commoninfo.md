# org.deepin.dde.control-center.commoninfo

通用信息配置资源，控制是否在开发者模式中显示只读保护选项。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `showReadOnlyProtection` | 只读保护显示开关 | 控制是否在开发者模式中显示只读保护选项 | bool | readwrite |

## 读写示例

```bash
# 查询只读保护显示开关
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center.commoninfo -k showReadOnlyProtection
# 设置只读保护显示开关
dde-dconfig set -a org.deepin.dde.control-center -r org.deepin.dde.control-center.commoninfo -k showReadOnlyProtection -v "<value>"
```

## 覆盖说明

- 该资源存在 Override 覆盖：`showReadOnlyProtection` 被 `org.deepin.dde.control-center/org.deepin.dde.control-center.commoninfo/100-commoninfo.json` 覆盖
