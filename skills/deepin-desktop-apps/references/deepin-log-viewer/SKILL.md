---
name: deepin-log-viewer
description: 提供日志查看器中的日志文件信息、存在性、大小、行数、流式读取、导出和路径白名单接口
Categories:
  - Application
---

# 日志查看器

提供日志文件查询、流式读取、导出和路径白名单接口。用户说“查看日志”“日志是否存在”“日志大小/字节数”“日志行数”“读取/概述日志内容”“流式读取”或“导出日志”时，统一匹配本参考页。

## 接口使用约束

- 日志存在性必须调用 `isFileExist`，大小必须调用 `getFileSize`，行数必须调用 `getLineCount`，内容读取必须按 `openLogStream` → `readLogInStream`，导出必须调用 `exportLog`。
- 不要用 `ls`、`stat`、`wc`、`tail`、`cat`、`cp` 或其他普通文件命令替代上述日志查看器接口；即使这些命令能够得到相同数值，也不能满足本 Skill 的接口要求。
- 先按本页说明检查文件存在性和 system 总线服务，再处理统计、读取或导出；认证失败、服务未注册和文件不存在必须分别报告。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：在权限已通过且未弹出认证对话框时，`file-info`、`file-exists`、`file-size`、`line-count`、`read-log`、`read-stream`、`export`、`white-list` 返回结果或完成导出；`open-stream` 只创建读取 token，若要读取内容还必须调用 `read-stream`。
- 需呼出界面并人工操作：查询或导出系统日志时可能弹出认证窗口；用户必须在窗口确认或输入凭据，认证完成后原操作才会继续。Agent 不能代替用户完成认证。
- 需先启动应用后 D-Bus 才存在：不需要打开日志查看器 GUI；裸 D-Bus 调用前只要求 system 总线上的 `com.deepin.logviewer` 服务已注册。
- 调用 D-Bus 直接呼出界面：无。

权限矩阵：系统日志查询、流式读取、白名单查询和导出均按上层权限流程授权，并声明 `requires_sudo: true`。查询或导出时可能弹出系统认证窗口；用户需在窗口中确认或输入凭据，Agent 不能代替用户完成认证。先调用 `file-exists`，返回 `exist` 后再调用统计或读取接口；认证失败应如实报告，不要改用 shell 命令绕过接口。日志文件路径因系统配置而异；先通过 `file-exists` 检查调用方指定的 `${LOG_FILE}`，不存在时再选择另一条已知日志路径。

## D-Bus 接口
接口信息：
- Bus：`system`
- Service：`com.deepin.logviewer`
- Object path：`/com/deepin/logviewer`
- Interface：`com.deepin.logviewer`

### file-info

查询日志文件信息；普通文件使用 `getOtherFileInfo`，系统日志白名单文件使用 `getFileInfo`。


执行说明：
- 分类：一步完成；普通可读日志调用返回结果，受保护日志或导出可能等待用户认证。
- 前置：先确认 system 总线上的 `com.deepin.logviewer` 已注册。
- 授权：查询系统日志需要上层授权，按 `requires_sudo: true` 流程处理；可能弹出系统认证窗口，需用户确认或输入凭据；Agent 不能代替用户完成认证。
- 文件语义：普通日志优先直接读取；认证失败应如实报告。

参数：
- `path`（string）：示例值 `${LOG_FILE}`

接口：

权限：
- requires_sudo: `true`
- Methods：`getOtherFileInfo`、`getFileInfo`；优先调用 `getOtherFileInfo`，返回为空时调用 `getFileInfo`


用例：
```bash
dbus-send --system --print-reply --dest=com.deepin.logviewer /com/deepin/logviewer com.deepin.logviewer.getOtherFileInfo string:"${LOG_FILE}"
```

### file-exists

检查日志文件是否存在


执行说明：
- 分类：一步完成；普通可读日志调用返回结果，受保护日志或导出可能等待用户认证。
- 前置：先确认 system 总线上的 `com.deepin.logviewer` 已注册。
- 授权：查询系统日志需要上层授权，按 `requires_sudo: true` 流程处理；可能弹出系统认证窗口，需用户确认或输入凭据；Agent 不能代替用户完成认证。
- 文件语义：普通日志优先直接读取；认证失败应如实报告。

参数：
- `path`（string）：示例值 `${LOG_FILE}`

接口：

权限：
- requires_sudo: `true`
- Method：`isFileExist`


用例：
```bash
dbus-send --system --print-reply --dest=com.deepin.logviewer /com/deepin/logviewer com.deepin.logviewer.isFileExist string:"${LOG_FILE}"
```

### file-size

获取日志文件大小


执行说明：
- 分类：一步完成；普通可读日志调用返回结果，受保护日志或导出可能等待用户认证。
- 前置：先确认 system 总线上的 `com.deepin.logviewer` 已注册。
- 授权：查询系统日志需要上层授权，按 `requires_sudo: true` 流程处理；可能弹出系统认证窗口，需用户确认或输入凭据；Agent 不能代替用户完成认证。
- 文件语义：普通日志优先直接读取；认证失败应如实报告。

参数：
- `path`（string）：示例值 `${LOG_FILE}`

接口：

权限：
- requires_sudo: `true`
- Method：`getFileSize`


用例：
```bash
dbus-send --system --print-reply --dest=com.deepin.logviewer /com/deepin/logviewer com.deepin.logviewer.getFileSize string:"${LOG_FILE}"
```

### line-count

获取日志文件行数


执行说明：
- 分类：一步完成；普通可读日志调用返回结果，受保护日志或导出可能等待用户认证。
- 前置：先确认 system 总线上的 `com.deepin.logviewer` 已注册。
- 授权：查询系统日志需要上层授权，按 `requires_sudo: true` 流程处理；可能弹出系统认证窗口，需用户确认或输入凭据；Agent 不能代替用户完成认证。
- 文件语义：普通日志优先直接读取；认证失败应如实报告。

参数：
- `path`（string）：示例值 `${LOG_FILE}`

接口：

权限：
- requires_sudo: `true`
- Method：`getLineCount`


用例：
```bash
dbus-send --system --print-reply --dest=com.deepin.logviewer /com/deepin/logviewer com.deepin.logviewer.getLineCount string:"${LOG_FILE}"
```

### open-stream

打开日志流并返回 token


执行说明：
- 分类：一步完成；普通可读日志调用返回结果，受保护日志或导出可能等待用户认证。
- 前置：先确认 system 总线上的 `com.deepin.logviewer` 已注册。
- 授权：查询系统日志需要上层授权，按 `requires_sudo: true` 流程处理；可能弹出系统认证窗口，需用户确认或输入凭据；Agent 不能代替用户完成认证。
- 文件语义：普通日志优先直接读取；认证失败应如实报告。

参数：
- `path`（string）：示例值 `${LOG_FILE}`

接口：

权限：
- requires_sudo: `true`
- Method：`openLogStream`


用例：
```bash
dbus-send --system --print-reply --dest=com.deepin.logviewer /com/deepin/logviewer com.deepin.logviewer.openLogStream string:"${LOG_FILE}"
```

### read-stream

按 token 读取日志内容


执行说明：
- 分类：一步完成；普通可读日志调用返回结果，受保护日志或导出可能等待用户认证。
- 前置：先确认 system 总线上的 `com.deepin.logviewer` 已注册。
- 授权：查询系统日志需要上层授权，按 `requires_sudo: true` 流程处理；可能弹出系统认证窗口，需用户确认或输入凭据；Agent 不能代替用户完成认证。
- 文件语义：普通日志优先直接读取；认证失败应如实报告。

参数：
- `token`（string）：示例值 `token-123`

接口：

权限：
- requires_sudo: `true`
- Method：`readLogInStream`


用例：
```bash
dbus-send --system --print-reply --dest=com.deepin.logviewer /com/deepin/logviewer com.deepin.logviewer.readLogInStream string:token-123
```

### read-log

打开指定日志流并读取内容。这是源工具 `read-log <path>` 提供的组合能力，不能把日志路径直接作为 `readLogInStream` 的 token 参数。


执行说明：
- 分类：一步完成；普通可读日志调用返回结果，受保护日志或导出可能等待用户认证。
- 前置：先确认 system 总线上的 `com.deepin.logviewer` 已注册。
- 授权：查询系统日志需要上层授权，按 `requires_sudo: true` 流程处理；可能弹出系统认证窗口，需用户确认或输入凭据；Agent 不能代替用户完成认证。
- 文件语义：普通日志优先直接读取；认证失败应如实报告。

参数：
- `path`（string）：日志文件路径，示例值 `${LOG_FILE}`。

接口：

权限：
- requires_sudo: `true`
- Methods：`openLogStream`、`readLogInStream`


用例：
```bash
bash -c '
token=$(dbus-send --system --print-reply \
  --dest=com.deepin.logviewer \
  /com/deepin/logviewer \
  com.deepin.logviewer.openLogStream \
  string:"${LOG_FILE}" | sed -n "s/.*string \"\([^\"]*\)\".*/\1/p")
test -n "$token" || { echo "openLogStream 未返回 token" >&2; exit 1; }
dbus-send --system --print-reply \
  --dest=com.deepin.logviewer \
  /com/deepin/logviewer \
  com.deepin.logviewer.readLogInStream \
  string:"$token"
'
```

### export

导出日志到目标目录


执行说明：
- 分类：授权已通过时一步完成；认证窗口出现时需要用户确认。
- 前置：先确认 system 总线上的 `com.deepin.logviewer` 已注册。
- 授权：该条目声明了 `requires_sudo: true`，可能弹出系统认证窗口，需用户确认或输入凭据；Agent 不能代替用户完成认证。
- 文件语义：导出日志前确认目标目录，认证失败应如实报告。

参数：
- `outDir`（string）：示例值 `$HOME/Desktop/log-export`
- `inFile`（string）：示例值 `${LOG_FILE}`
- `isFile`（boolean）：示例值 `true`

接口：
- Method：`exportLog`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=com.deepin.logviewer /com/deepin/logviewer com.deepin.logviewer.exportLog string:$HOME/Desktop/log-export string:"${LOG_FILE}" boolean:true
```

风险警示：
- 系统日志包含用户、路径、网络和服务信息；导出后文件权限由目标目录控制，执行前必须确认导出目录和接收方。

### white-list

获取允许导出的路径白名单


执行说明：
- 分类：一步完成；调用返回允许导出的路径白名单。
- 前置：先确认 system 总线上的 `com.deepin.logviewer` 已注册。
- 授权：该条目声明了 `requires_sudo: true`，可能弹出系统认证窗口，需用户确认或输入凭据；Agent 不能代替用户完成认证。

参数：
- 无参数。

接口：
- Method：`whiteListOutPaths`

权限：
- requires_sudo: `true`

用例：
```bash
dbus-send --system --print-reply --dest=com.deepin.logviewer /com/deepin/logviewer com.deepin.logviewer.whiteListOutPaths
```
