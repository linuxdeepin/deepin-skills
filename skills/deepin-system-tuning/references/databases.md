# 数据库调优边界

本技能只调优已安装的服务型数据库配置，不初始化、不迁移、不连接业务库、不修改口令或数据目录。SQLite 和 Redis 只提供建议，因为它们的参数取决于应用连接方式、持久化策略和业务容忍度。

## PostgreSQL

检测条件：

- 存在 `/etc/postgresql/<版本>/main/postgresql.conf`。
- 该文件包含 `include_dir`，且指向一个可用于 drop-in 的目录（通常是 `conf.d`）。
- 目录不存在时会在用户授权执行时创建；没有 `include_dir` 时只给 advisory，不修改主配置文件。
- 服务单元优先使用探测到的 `postgresql@<版本>-main.service`，即使该实例当前为 inactive 或 failed；只有实例单元不存在时才回退到 `postgresql.service`。

写入 `/etc/postgresql/<版本>/main/conf.d/90-deepin-tuning.conf`，按总内存计算：

| 参数 | 公式 | 约束 |
| --- | --- | --- |
| `shared_buffers` | 25% RAM | 128 MiB–4 GiB |
| `effective_cache_size` | 50% RAM | 512 MiB–12 GiB |
| `maintenance_work_mem` | RAM/16 | 64 MiB–1 GiB |
| `work_mem` | RAM/(100×4) | 4 MiB–64 MiB |
| `max_connections` | 100 | 固定保守值 |
| `random_page_cost` | 1.1 | SSD/NVMe 常用值 |
| `effective_io_concurrency` | 200 | NVMe/SSD |
| `wal_compression` | on | 兼容现代版本 |
| `checkpoint_completion_target` | 0.9 | 降低突发 I/O |
| `default_statistics_target` | 100 | 保守值 |

`shared_buffers` 需要重启 PostgreSQL 才生效；`effective_cache_size` 等可 reload。`apply` 默认只写文件并尝试 reload，状态为 `applied_pending_restart`；显式加 `--allow-service-restart` 才会重启。执行前应告知用户数据库会短暂不可用。

不设置 `fsync=off`、`synchronous_commit=off`、`full_page_writes=off` 等牺牲持久性的参数。

## MariaDB / MySQL

检测到 `/etc/mysql/mariadb.conf.d` 或 `/etc/mysql/conf.d` 才生成写入项；只有客户端目录不算服务端安装。只有 `include_dirs` 且存在服务端二进制或服务单元时才视为安装；仅有客户端目录不算服务端。写入 `<include_dir>/90-deepin-tuning.cnf`：

| 参数 | 公式 | 约束 |
| --- | --- | --- |
| `innodb_buffer_pool_size` | 25% RAM | 128 MiB–8 GiB |
| `innodb_log_file_size` | RAM/32 | 128 MiB–1 GiB |
| `innodb_buffer_pool_instances` | ceil(pool GiB) | 仅 MySQL 或 MariaDB < 10.6；MariaDB 10.6+ 已移除该变量，版本未知时也不写入 |
| `innodb_flush_method` | `O_DIRECT` | Linux |
| `innodb_flush_log_at_trx_commit` | 1 | 保持事务持久性 |
| `max_connections` | 151 | 保守值 |
| `table_open_cache` | 4000 | 中等规模 |
| `tmp_table_size` / `max_heap_table_size` | 64M | 防止内存临时表过大 |
| `join_buffer_size` | 4M | 保守值 |

这些参数大多需要重启 MariaDB/MySQL。脚本不会自动重启，除非用户显式 `--allow-service-restart`；即使如此也只重启数据库单元，不重启系统。重启前若检测到 MySQL 8 的 `--validate-config`，会先校验配置；校验失败或重启失败会被标记为失败并触发文件恢复，而不是静默保留一个无法启动的配置。恢复阶段如果数据库服务仍未运行，会保持 `needs_attention`/`rolled_back_pending`，再次恢复会重试重启并检查 `is-active`，不会把待重启项直接当成已恢复。MariaDB 不提供通用 `--validate-config`，通过产品/版本过滤避免写入已移除变量。

## Redis

检测到 `/etc/redis/redis.conf` 时只给 advisory。原因：

- `maxmemory` 需要结合是否共享实例、持久化方式和淘汰策略。
- 盲目设置 `maxmemory` 可能导致写入失败或键被淘汰。
- 不自动修改 `appendonly`、`save` 或 `requirepass`。

需要调优时，先让用户确认业务容忍度，再手工修改；本技能不提供任意 `redis-cli` 写入。

## SQLite

检测到 `sqlite3` 只说明本机有 SQLite 工具，不代表有服务端数据库。advisory 会建议评估：

- `PRAGMA journal_mode=WAL`：改善并发读写，但需要应用接受 WAL 文件。
- `PRAGMA synchronous=NORMAL`：降低 fsync 次数，断电时可能丢失最近事务；不能默认用于关键数据。
- `PRAGMA cache_size`、`PRAGMA mmap_size`：按应用内存预算设置。
- 不要对生产库盲目关闭同步或启用 `locking_mode=EXCLUSIVE`。

## 验证限制

本技能不连接数据库，因此：

- `verify` 能验证配置文件摘要是否与计划一致。
- 不能验证 SQL 层参数是否已被运行中的服务加载。
- `applied_pending_restart` 表示“文件已写，但运行态未确认”；重启后应重新 `verify` 并查看数据库日志。
- 如果数据库服务未运行，reload 会失败，配置仍保留为待重启状态；不要把它报告成已生效。
