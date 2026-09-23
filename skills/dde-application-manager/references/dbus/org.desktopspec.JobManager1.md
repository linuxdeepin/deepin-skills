# org.desktopspec.JobManager1 接口参考

该接口提供应用启动任务跟踪能力。所有可能阻塞的方法都会返回一个实现 `org.desktopspec.JobManager1.Job` 接口的对象路径，通过本接口的信号可以监控任务状态。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationManager1` |
| Object path | `/org/desktopspec/JobManager1` |
| Interface | `org.desktopspec.JobManager1` |
| Bus | Session |

### 信号

#### JobNew

新任务创建时发出。

- **参数**: `job`（object path, 类型 `o`）：任务对象路径；`source`（object path, 类型 `o`）：产生该任务的源对象路径

```bash
gdbus monitor --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/JobManager1
```

#### JobRemoved

任务移除时发出。

- **参数**: `job`（object path, 类型 `o`）：任务对象路径；`status`（string, 类型 `s`）：任务最终状态（`started`/`running`/`finished`/`suspend`/`canceled`）；`result`（variant 数组, 类型 `av`）：任务结果

```bash
gdbus monitor --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/JobManager1
```

---
