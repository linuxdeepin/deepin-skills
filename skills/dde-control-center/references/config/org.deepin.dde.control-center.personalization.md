# org.deepin.dde.control-center.personalization

个性化配置资源，管理需要在个性化设置中隐藏的图标主题列表。

## 配置项

| Key | Name | Description | 类型 | Permissions |
|---|---|---|---|---|
| `hideIconThemes` | 隐藏图标主题 | 配置需要在个性化设置中隐藏的图标主题列表 | array | readonly |

## 读写示例

```bash
# 查询隐藏图标主题
dde-dconfig get -a org.deepin.dde.control-center -r org.deepin.dde.control-center.personalization -k hideIconThemes
```
