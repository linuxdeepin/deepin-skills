# org.desktopspec.JobManager1.Job 接口参考

该接口提供单个异步任务的管理能力。所有可能阻塞的 D-Bus 方法会返回一个实现此接口的对象路径，调用方可通过该接口查询任务状态、取消或暂停/恢复任务。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationManager1` |
| Object path | `<dynamic>` |
| Interface | `org.desktopspec.JobManager1.Job` |
| Bus | Session |

### 任务操作

#### Cancel

取消该任务。成功调用后任务状态变为 `canceled`，随后任务被移除，`JobManager1` 接口发出 `JobRemoved` 信号。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.desktopspec.JobManager1.Job.Cancel
```

#### Suspend

暂停该任务。成功调用后任务状态先变为 `suspending`，随后变为 `suspended`。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.desktopspec.JobManager1.Job.Suspend
```

#### Resume

恢复已暂停的任务。成功调用后恢复异步计算，任务状态变为 `running`。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.desktopspec.JobManager1.Job.Resume
```

### 任务属性

#### Status（属性）

任务当前状态。取值为 `pending`、`running`、`suspending`、`suspended`、`canceled`、`finished`、`failed`。

| 属性 | 值 |
|------|------|
| 类型 | `s` |
| 读写权限 | read |

读取示例：

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path <dynamic> \
  --method org.freedesktop.DBus.Properties.Get \
  org.desktopspec.JobManager1.Job Status
```
