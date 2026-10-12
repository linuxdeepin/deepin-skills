# org.deepin.dde.Daemon1 接口参考

该接口提供系统级守护进程管理和调试能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Daemon1` |
| Object path | `/org/deepin/dde/Daemon1` |
| Interface | `org.deepin.dde.Daemon1` |
| Bus | Session |
### 守护进程方法

#### CallTrace

调用跟踪。

- **功能**：输出当前 D-Bus 调用栈跟踪信息，用于调试。
- **触发条件**：当需要排查 D-Bus 调用链路问题时调用。
- **使用场景**：开发调试、问题排查。

- **输入参数**: `times`（uint32, 类型 `u`）：采样次数；`seconds`（uint32, 类型 `u`）：采样间隔秒数
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Daemon1 \
  --object-path /org/deepin/dde/Daemon1 \
  --method org.deepin.dde.Daemon1.CallTrace 10 5
```

#### StartPart2

启动第二阶段。

- **功能**：启动守护进程第二阶段初始化，加载依赖 Session 总线的模块。
- **触发条件**：在系统启动第一阶段完成后由启动流程调用。
- **使用场景**：系统启动流程中分阶段加载守护进程服务。

- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.Daemon1 \
  --object-path /org/deepin/dde/Daemon1 \
  --method org.deepin.dde.Daemon1.StartPart2
```


## 兼容性接口

`org.dde.session.Daemon1` 是旧版兼容服务名，与 `org.deepin.dde.Daemon1`（Session 总线）提供相同的 CallTrace、StartPart2 方法，保留此服务名别名以兼容历史调用方。新代码应推荐使用 `org.deepin.dde.Daemon1`。
