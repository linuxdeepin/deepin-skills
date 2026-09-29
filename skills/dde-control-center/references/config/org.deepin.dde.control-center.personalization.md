# org.deepin.dde.control-center.personalization

个性化配置资源，管理控制中心个性化设置中的图标主题隐藏配置。

## 配置项

| Key | Name | Description | 类型 | 取值范围 | Permissions | Flags |
|---|---|---|---|---|---|---|
| `hideIconThemes` | 隐藏图标主题 | 配置需要在个性化设置中隐藏的图标主题列表 | array | 字符串数组（图标主题名列表） | readonly | global |

## 读写示例

```bash
# 查询隐藏图标主题
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center.personalization -k hideIconThemes
```
