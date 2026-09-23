# org.desktopspec.ApplicationUpdateNotifier1 接口参考

该接口提供应用更新完成通知能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationUpdateNotifier1` |
| Object path | `/org/desktopspec/ApplicationUpdateNotifier1` |
| Interface | `org.desktopspec.ApplicationUpdateNotifier1` |
| Bus | Session |


### 应用更新信号

#### ApplicationUpdated

应用更新完成时发出。

- **参数**: 无
- **触发条件**: 应用更新完成时发出

```bash
gdbus monitor --session \
  --dest org.desktopspec.ApplicationUpdateNotifier1 \
  --object-path /org/desktopspec/ApplicationUpdateNotifier1
```

