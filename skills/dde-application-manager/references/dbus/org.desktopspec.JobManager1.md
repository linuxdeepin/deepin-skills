# org.desktopspec.JobManager1 接口参考

该接口提供应用启动任务跟踪能力。所有可能阻塞的 D-Bus 方法会返回一个实现 `org.desktopspec.JobManager1.Job` 接口的对象路径，调用方可通过本接口的信号监听任务状态变化。

任务对象本身实现 `org.desktopspec.JobManager1.Job` 接口，提供状态查询和取消/暂停/恢复操作，详见 [org.desktopspec.JobManager1.Job.md](org.desktopspec.JobManager1.Job.md)。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationManager1` |
| Object path | `/org/desktopspec/ApplicationManager1/JobManager1` |
| Interface | `org.desktopspec.JobManager1` |
| Bus | Session |

### 任务信号

#### JobNew

新任务创建时发出。调用可能阻塞的方法（如 `Launch`）后，任务对象创建时触发此信号。

- **参数**:
  - `job`（object path, 类型 `o`）：任务对象路径
  - `source`（object path, 类型 `o`）：产生该任务的 D-Bus 对象路径

监听示例：

```bash
gdbus monitor --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/JobManager1
```

#### JobRemoved

任务完成移除时发出。任务执行完毕、被取消或出错后触发此信号。

- **参数**:
  - `job`（object path, 类型 `o`）：任务对象路径
  - `status`（string, 类型 `s`）：任务最终状态，取值为 `pending`、`running`、`suspending`、`suspended`、`canceled`、`finished`、`failed`
  - `result`（数组, 类型 `av`）：任务结果，调用方需遍历列表判断值的有效性

监听示例：

```bash
gdbus monitor --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1/JobManager1
```
