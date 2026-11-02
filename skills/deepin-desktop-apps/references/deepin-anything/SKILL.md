---
name: deepin-anything
description: 提供基于文件名索引的关键词搜索、通配符搜索（`-w`）和 systemd 服务状态查询接口
Categories:
  - Application
---

# 极速文件搜索

提供基于文件名索引的关键词搜索和通配符搜索接口；不负责文件内容全文搜索或全文索引开关管理。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：`search`、`wildcard` 返回搜索结果，`status` 返回服务状态。
- 需呼出界面并人工操作：无。
- 需先启动应用后 D-Bus 才存在：不适用；本 Skill 不调用 D-Bus，只要求 `deepin-anything-searcher` 和 `deepin-anything-server` 可用。
- 调用 D-Bus 直接呼出界面：无。

## CLI 命令

### search

搜索文件名包含关键词的文件


执行说明：
- 分类：一步完成；命令返回后取得该接口结果或提交请求。
- 前置：不依赖 D-Bus；确保对应 CLI 和当前桌面会话可用。

参数：
- `path`（string）：示例值 `$HOME/Documents`
- `keyword`（string）：示例值 `report`

用例：
```bash
deepin-anything-searcher $HOME/Documents report
```

### wildcard

按通配符搜索文件名


执行说明：
- 分类：一步完成；命令返回后取得该接口结果或提交请求。
- 前置：不依赖 D-Bus；确保对应 CLI 和当前桌面会话可用。

参数：
- `path`（string）：示例值 `$HOME/Documents`
- `pattern`（string）：示例值 `*.pdf`；`wildcard` 使用 `deepin-anything-searcher -w`，只匹配文件名，不读取文件内容。

用例：
```bash
deepin-anything-searcher -w $HOME/Documents '*.pdf'
```

### status

查询 deepin-anything 索引服务的 systemd 状态。


执行说明：
- 分类：一步完成；命令返回后取得该接口结果或提交请求。
- 前置：不依赖 D-Bus；确保对应 CLI 和当前桌面会话可用。

参数：
- 无参数。

用例：
```bash
systemctl status deepin-anything-server
```
