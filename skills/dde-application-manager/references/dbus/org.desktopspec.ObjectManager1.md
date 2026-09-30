# org.desktopspec.DBus.ObjectManager 接口参考

该接口提供应用对象管理能力。通过标准的 D-Bus ObjectManager 接口，调用方可查询所有已注册的应用对象，并监听应用对象的添加和移除事件。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationManager1` |
| Object path | `/org/desktopspec/ApplicationManager1` |
| Interface | `org.desktopspec.DBus.ObjectManager` |
| Bus | Session |

### 对象管理操作

#### GetManagedObjects

返回所有已注册应用对象及其接口和属性。调用此方法可一次性获取应用管理器中所有应用的对象路径、实现的接口列表和对应的属性值。

- **输入参数**: 无
- **返回值**: `a{oa{sa{sv}}}`（字典）：以对象路径为键，每个对象路径对应的值为接口名到属性映射的字典

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1 \
  --method org.desktopspec.DBus.ObjectManager.GetManagedObjects
```

### 对象管理信号

#### InterfacesAdded

新应用对象被添加时发出。当应用管理器注册新应用（如安装新应用或重新加载应用列表）后触发此信号。

- **参数**:
  - `object_path`（object path, 类型 `o`）：新添加的应用对象路径
  - `interfaces_and_properties`（字典, 类型 `a{sa{sv}}`）：该对象实现的接口名到属性映射的字典

监听示例：

```bash
gdbus monitor --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1
```

#### InterfacesRemoved

应用对象被移除时发出。当应用管理器注销应用（如卸载应用或重新加载应用列表）后触发此信号。

- **参数**:
  - `object_path`（object path, 类型 `o`）：被移除的应用对象路径
  - `interfaces`（数组, 类型 `as`）：该对象上被移除的接口名列表

监听示例：

```bash
gdbus monitor --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/ApplicationManager1
```
