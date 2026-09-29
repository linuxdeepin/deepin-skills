# org.deepin.dde.InhibitHint1 接口参考

该接口提供抑制提示（Inhibit Hint）信息查询能力，用于向调用方提供本地化的抑制提示名称、图标和原因。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.InhibitHint1` |
| Object path | `/org/deepin/dde/InhibitHint1` |
| Interface | `org.deepin.dde.InhibitHint1` |
| Bus | Session |

## 兼容性说明（兼容）

该接口以库形式实现，由调用方在自己的进程中注册导出，而非独立服务进程，因此无独立 D-Bus 激活文件。接口提供 `Get` 方法，根据 locale 和抑制原因返回本地化的提示信息（名称、图标、原因）。该接口保留用于兼容旧版抑制提示机制，不建议在新代码中使用。

