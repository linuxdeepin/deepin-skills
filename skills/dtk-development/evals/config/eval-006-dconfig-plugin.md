# Eval: 插件场景下 DConfig appId 与 configId 命名

## 任务

一个 dde-control-center 插件（插件名 `myplugin`）需要使用 DConfig 存储自身
配置。说明 appId 和 configId 应如何确定，给出 C++ 创建代码，并说明 meta 文件
的安装路径。

## 期望输出

回答应明确：

1. appId 是宿主应用 `org.deepin.dde.control-center`，不是插件自身的标识。
   插件不是独立应用，不能为它单独构造 appId。
2. configId 是 `org.deepin.dde.control-center.myplugin`，在宿主命名空间下
   增加插件标识后缀，不使用 `settings` 等泛化名称。
3. 使用 `DConfig::create("org.deepin.dde.control-center",
   "org.deepin.dde.control-center.myplugin", QString(), this)` 创建对象，
   不使用默认构造函数。
4. meta 文件安装到
   `/usr/share/dsg/configs/org.deepin.dde.control-center/org.deepin.dde.control-center.myplugin.json`。
5. 配置不可用时使用 fallback 默认值，不阻塞插件加载。

## 验证要点

- [ ] appId 使用宿主应用的标识，不是插件名或插件自行构造的 ID
- [ ] configId 在宿主命名空间下，使用倒置域名 + 插件后缀
- [ ] 使用 `DConfig::create()` 显式传入 appId，不使用默认构造函数
- [ ] meta 文件安装路径中 appId 和 configId 正确对应
- [ ] 配置不可用时有 fallback，不阻塞
- [ ] 未使用 QSettings 替代 DConfig

## 评分标准

| 等级 | 条件 |
|------|------|
| ✅ **PASS** | 所有验证要点全部满足，代码可编译或语法正确 |
| ⚠️ **PARTIAL** | appId 或 configId 之一正确，但创建方式或安装路径有误 |
| ❌ **FAIL** | 为插件单独构造 appId，或使用泛化 configId，或使用默认构造函数 |

## 反模式检查

- [ ] 未为插件单独构造 appId
- [ ] 未使用 `settings`、`example` 等泛化名称作为 configId
- [ ] 未使用默认构造函数 `new DConfig(configId, ...)` 创建插件配置
- [ ] 未使用 QSettings 替代 DConfig
- [ ] 配置服务不可用时未阻塞插件加载（应有 fallback）
