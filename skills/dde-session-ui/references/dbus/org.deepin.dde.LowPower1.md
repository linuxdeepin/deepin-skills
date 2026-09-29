# org.deepin.dde.LowPower1 接口参考

该接口提供低电量提示窗口的显示控制能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.LowPower1` |
| Object path | `/org/deepin/dde/LowPower1` |
| Interface | `org.deepin.dde.LowPower1` |
| Bus | Session |

### Raise

将低电量提示窗口提升到最前层。

- **功能**: 将低电量提示窗口提升到所有窗口的最上层，确保用户能看到低电量警告
- **触发条件**: 由系统电源管理组件主动调用，当低电量提示窗口被其他窗口遮挡时触发
- **使用场景**: 系统检测到电池电量低于阈值时弹出低电量提示，需要确保提示窗口在最前层
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LowPower1 \
  --object-path /org/deepin/dde/LowPower1 \
  --method org.deepin.dde.LowPower1.Raise
```

### Quit

退出低电量提示程序。

- **功能**: 关闭低电量提示窗口并退出低电量提示程序进程
- **触发条件**: 由系统电源管理组件主动调用，当低电量条件消除（如接通电源）或用户确认后触发
- **使用场景**: 用户接通电源充电后，系统关闭低电量提示窗口
- **输入参数**: 无
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.deepin.dde.LowPower1 \
  --object-path /org/deepin/dde/LowPower1 \
  --method org.deepin.dde.LowPower1.Quit
```
