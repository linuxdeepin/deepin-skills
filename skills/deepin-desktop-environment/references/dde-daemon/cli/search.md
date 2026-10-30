# search 服务说明

当前用户的字符串候选搜索服务，不是文件全文搜索命令。

## 基本信息

| 字段 | 值 |
|------|------|
| 所属包名 | `dde-daemon` |
| 安装路径 | `/usr/lib/deepin-daemon/search` |
| DDE 角色 | `org.deepin.dde.Search1` 会话服务进程 |

服务接收调用方提供的字符串列表或字典，生成可用于中文拼音与模糊匹配的用户缓存。它不负责扫描文件系统或建立文件内容索引；没有数据集时不能直接搜索系统文件。

通常通过 D-Bus 激活，无需重复手动启动。调用方式见 [Search1 接口](../dbus/org.deepin.dde.Search1.md)。
