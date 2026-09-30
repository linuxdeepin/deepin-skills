# org.desktopspec.ApplicationUpdateNotifier1 接口参考

该接口提供应用更新完成通知能力。当应用信息需要更新时（如应用安装、卸载或更新后），通过此接口发出信号通知其他组件刷新应用信息。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationUpdateNotifier1` |
| Object path | `/org/desktopspec/ApplicationUpdateNotifier1` |
| Interface | `org.desktopspec.ApplicationUpdateNotifier1` |
| Bus | System |

### 应用更新信号

#### ApplicationUpdated

应用更新完成时发出。当应用信息需要更新时触发，通知监听方重新加载应用列表或刷新应用属性。

- **参数**: 无

监听示例：

```bash
gdbus monitor --system \
  --dest org.desktopspec.ApplicationUpdateNotifier1 \
  --object-path /org/desktopspec/ApplicationUpdateNotifier1
```
