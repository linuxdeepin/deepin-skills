# 方案矩阵与推荐规则

方案是语义操作集合，不是预设 shell 脚本。同一方案在不同机器上会自动省略不可用项（例如没有电池时不提供续航方案，没有 Wi-Fi 时不写 NetworkManager 片段）。

## 动作矩阵

| 方案 | 电源 | 内核/服务 | 图形环境 | 备注 |
| --- | --- | --- | --- | --- |
| `office` | DDE `balance`，关闭省电，允许高性能 | fstrim.timer（SSD/NVMe） | VA-API、`mesa_glthread=true`、动画开 | 最低风险，适合日常 |
| `programming` | 交流电 `performance`，电池 `balance` | inotify 524288/8192/65536、max_map_count 1048576、swappiness（zram 100，否则 10）、vfs_cache_pressure 50、dirty 5/10、file-max 2097152、somaxconn 4096；limits nofile 65536；fstrim；irqbalance/thermald 若已安装 | VA-API、GL 线程 | 不含数据库；系统项需 root |
| `performance` | DDE `performance` | swappiness（zram 100，否则 10）、vfs 50、dirty 5/10；fstrim；irqbalance/thermald；Wi-Fi powersave=2 | VA-API、GL 线程 | modprobe 关闭 iwlwifi/音频省电，重启后生效 |
| `render-quality` | 不改电源 | fstrim | VA-API、GL 线程、Mesa 着色器缓存 2G / NVIDIA 磁盘缓存、动画开 | 高分屏优先，可与 `programming` 组合 |
| `render-performance` | 交流电 `performance`，电池 `balance` | fstrim；Wi-Fi powersave=2 | VA-API、GL 线程、着色器缓存、动画关 | 低延迟交互 |
| `gaming` | DDE `performance` | max_map_count、swappiness（zram 100，否则 10）；fstrim；irqbalance/thermald；Wi-Fi powersave=2 | 着色器缓存、动画关；PRIME 仅给按应用建议 | 集显也保留基础项 |
| `battery` | DDE `powersave`、省电开、高性能关 | laptop_mode 5、dirty_writeback 6000、dirty_expire 12000；有 zram 时 swappiness 100；Wi-Fi powersave=3 | VA-API、GL 线程关、动画关 | modprobe iwlwifi/音频/PSR 省电，重启后生效 |
| `database` | 不改电源 | 仅已安装的 PostgreSQL/MariaDB 配置 | 不改 | Redis/SQLite 只给建议 |

`programming` 只在交流电时使用性能电源；电池时用 `balance`，避免把“编程”误解成“始终满功耗”。

## 独立组件

如果不想一次套用整套方案，可以只选一个或多个组件：

| 组件 | 范围 |
| --- | --- |
| `power-performance` | 只切换电源后端到性能模式 |
| `power-balanced` | 只切换电源后端到均衡模式 |
| `power-battery` | 只切换电源后端到省电模式 |
| `graphics-quality` | 只配置图形环境变量、着色器缓存和动画 |
| `graphics-performance` | 只配置图形环境变量、GL 线程和关闭动画 |
| `dev-limits` | 只配置 sysctl、PAM limits、TRIM 和可选多核服务 |
| `database-auto` | 只配置已安装数据库的 drop-in |

这些组件不参与默认推荐排序，避免候选列表膨胀；`catalog` 的 `components` 字段和 `plan --profiles` 可直接使用。组件与整套方案可以混合，冲突仍按同一键规则检查。

## 推荐评分

`recommend` 用硬件、电源、会话和 `--context` 做启发式排序：

- `intent`：`coding`、`office`、`gaming`、`battery`、`rendering`、`database` 等；命中时加分。
- `power_source`：`ac` 提高 `performance`/`gaming`，`battery` 提高 `battery` 并降低性能方案。
- `priority`：`performance` 提高性能/低延迟，`quality` 提高画质，`quiet` 提高办公。
- 硬件：内存 ≥ 12 GiB、≥ 12 逻辑核、NVMe、独显、高分辨率/高刷新率分别给对应方案加分。
- 可用性：没有电池不推荐 `battery`；没有 PostgreSQL/MariaDB/Redis 不推荐 `database`；SQLite 只提供使用建议。
- 评分上限 100，`fit` 为 `high`/`medium`/`low`。排序是建议，不是基准测试结论。

输出中的每个选项包含 `operation_count`、`advisory_count`、`requires_root`、`requires_reboot`、`requires_relogin`，用于向用户说明代价。`--all` 会显示不可用项及原因，便于解释“为什么没有推荐数据库/续航”。

## 组合与冲突

```bash
tune.py plan --profiles programming,render-quality
```

合并规则：

- 同一 gsettings 键、同一服务单元、同一 sysctl 键、同一文件路径的相同目标会去重。
- 同一键的不同目标产生 `conflicts`，整个计划 `execute_ready=false`。例如 `performance` 与 `battery` 的电源模式冲突。
- 文件按托管块合并，保留标记外的内容和旧块中未被新方案覆盖的键；同一键不同值视为冲突。
- advisory 项不参与执行，只用于说明。

不要为了让冲突消失而修改计划 JSON、删除状态记录或直接覆盖系统文件。应让用户选择其中一个方案，或使用 `--user-only` 先做低风险部分。

## 组件化选择

- 电源：`office`、`performance`、`battery`、`gaming` 之一。
- 图形：`render-quality` 或 `render-performance`；`render-quality` 不改电源，便于叠加。
- 开发限制：`programming`，不自动包含数据库。
- 数据库：显式选择 `database`；只在检测到 PostgreSQL/MariaDB/MySQL 服务时可用。

图形环境变量按实际 GPU 厂商校验；混合 NVIDIA 的 PRIME 不写入全局环境，而建议用 `prime-run` 或按应用设置。zram 存在时 swappiness 使用更高值，否则使用保守的 10（电池默认不改）。

## 建议的沟通方式

1. 先给 2–4 个候选，不只给一个“最优”；说明评分理由和代价。
2. 明确哪些项需要 root、重启、重新登录或数据库服务重启。
3. 用户选择后再 `plan`，展示逐项命令和 `execute_ready`。
4. 执行后看 `verify`，区分“配置文件已写”和“运行态已生效”。
5. 用户不满意时用 `rollback`，不要手工删文件或改回 gsettings。


## 桌面组合场景

| ID | 独立组件与策略 |
| --- | --- |
| `comfort-office` | 均衡电源、图形质量、主屏原生模式、保留特效、区分 AC/电池的空闲行为 |
| `coding-smooth` | 开发限制、图形性能、当前分辨率最高刷新率、减少特效；AC 性能电源，电池均衡 |
| `long-battery` | 省电电源、减少 GL 线程、当前分辨率最低刷新率、主屏亮度不高于 0.55、减少特效、电池空闲策略；关闭自动亮度并将省电亮度衰减设为 0，避免双重调节 |
| `gaming-low-latency` | 性能电源、图形性能、当前分辨率最高刷新率、减少特效；不全局强制独显 |
| `design-accurate` | 均衡电源、图形质量、主屏原生模式、保留特效、关闭自动色温；不等于显示器校色 |

显示组件只操作主屏；多屏逐屏偏好通过 --settings.outputs 指定。最低/最高刷新率都从当前分辨率的实际 Modes 中选择；没有低刷模式时保持原模式，不降分辨率凑低刷。原生模式取服务 BestMode。

`effects-reduced` 关闭已探测到的模糊和窗口动画，保留合成；KWin 使用当前会话加载/卸载接口，Treeland 使用白名单 dconfig，后者不宣称消费者运行态已验证。`idle-balanced` 的 AC 熄屏/休眠/锁屏为 900/1800/900 秒，电池为 180/900/180 秒；`idle-battery` 仅修改电池部分。组件所需接口不可用时给 advisory，显式设置不可用时 blocked。

组合候选参与推荐，但硬件评分只反映适配线索；实际可执行性由 plan 的 blocked/conflicts 决定。--settings 可以显式覆盖同一语义键，其他冲突继续拒绝。详细语义、范围、跨设置约束及显示确认流程见 [desktop.md](desktop.md)。
