# org.desktopspec.ApplicationManager1 接口参考

该接口提供应用列表查询、应用识别、用户应用增删和应用执行能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationManager1` |
| Object path | `/org/desktopspec/ApplicationManager1` |
| Interface | `org.desktopspec.ApplicationManager1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 应用管理操作

#### ReloadApplications

重新加载应用列表。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.desktopspec.ApplicationManager1.ReloadApplications
```

#### Identify

通过 pidfd 识别应用。

- **输入参数**: `pidfd`（handle, 类型 `h`）：进程文件描述符
- **返回值**: `(s,o,a{sa{sv}})`（元组）：应用 ID、对象路径和属性

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.desktopspec.ApplicationManager1.Identify 0
```

#### addUserApplication

添加用户应用。

- **输入参数**: `desktop_file`（字典, 类型 `a{sv}`）：桌面文件内容；`name`（string, 类型 `s`）：应用名称
- **返回值**: `s`（string）：应用 ID

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.desktopspec.ApplicationManager1.addUserApplication "<desktop_file>" "myapp"
```

#### deleteUserApplication

删除用户应用。

- **输入参数**: `app_id`（string, 类型 `s`）：应用 ID
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.desktopspec.ApplicationManager1.deleteUserApplication "myapp"
```

#### executeCommand

执行命令。

- **输入参数**: `program`（string, 类型 `s`）：程序名；`arguments`（数组, 类型 `as`）：参数列表；`type`（string, 类型 `s`）：类型；`runId`（string, 类型 `s`）：运行 ID；`envVars`（字典, 类型 `a{ss}`）：环境变量；`workdir`（string, 类型 `s`）：工作目录
- **返回值**: `o`（object path）：任务路径

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.desktopspec.ApplicationManager1.executeCommand
```


### 应用列表属性

#### List（属性）

应用列表。

| 属性 | 值 |
|------|------|
| 类型 | `ao` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.ApplicationManager1 List
```
