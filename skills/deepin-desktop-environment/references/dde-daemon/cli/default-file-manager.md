# default-file-manager 命令参考

启动当前用户配置的默认文件管理器。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-daemon` |
| 安装路径 | `/usr/lib/deepin-daemon/default-file-manager` |
| DDE 角色 | 默认文件管理器启动工具 |

## 用途

查询目录 MIME 类型对应的默认文件管理器，并通过应用管理器启动。该工具不修改默认文件管理器关联，不接收用于设置默认应用的参数。

## 使用示例

在当前用户的 DDE 图形会话中运行：

```bash
/usr/lib/deepin-daemon/default-file-manager
```
