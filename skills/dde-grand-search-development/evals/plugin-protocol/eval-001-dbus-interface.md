# Eval: 实现 V1.0 三个 DBus 接口

## 任务

创建一个全局搜索插件，实现 V1.0 协议要求的全部 DBus 接口。请给出 Adaptor 定义与 `main()` 中的服务注册代码。

## 期望输出

回答应：
1. 实现 `Search(String)→String`、`Stop(String)→Boolean`、`Action(String)→Boolean` 三个方法，方法名大小写正确
2. 使用 `QDBusAbstractAdaptor` 子类，通过 `Q_CLASSINFO("D-Bus Interface", ...)` 声明接口名，并给出 `D-Bus Introspection` 元数据
3. 在 `main()` 中使用 `QDBusConnection::sessionBus()` 注册服务与对象
4. Adaptor 以导出对象为父对象
5. 服务名、对象路径、接口名与 `.conf` 三要素保持一致

## 验证要点

- [ ] 三个方法名分别为 `Search`/`Stop`/`Action`（首字母大写）
- [ ] 签名正确：`Search(s)→s`、`Stop(s)→b`、`Action(s)→b`
- [ ] 使用 `QDBusAbstractAdaptor` 与 `Q_CLASSINFO("D-Bus Interface", ...)`
- [ ] 使用 `QDBusConnection::sessionBus()`，而非 `systemBus()`
- [ ] `registerService` 与 `registerObject` 均被调用，且参数与 conf 一致
- [ ] Adaptor 是导出对象的子对象
- [ ] 服务注册失败时程序退出而不是继续运行

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 三个接口签名与名称正确，会话总线注册，Adaptor 父子关系正确，且处理注册失败 |
| ⚠️ **PARTIAL** | 接口实现正确但注册到系统总线，或 Adaptor 父子关系错误 |
| ❌ **FAIL** | 方法名或签名错误，或未实现三个接口中的任何一个 |

## 反模式检查

- [ ] 未使用 `QDBusConnection::systemBus()`
- [ ] 未把方法名写成 `search`/`stop`/`action` 等小写形式
- [ ] 未把 Adaptor 定义成非 `QDBusAbstractAdaptor` 的普通 QObject
- [ ] 未遗漏 `Q_OBJECT` 宏
