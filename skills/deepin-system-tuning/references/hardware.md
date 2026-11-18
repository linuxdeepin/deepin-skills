# 硬件探测与分类

`tune.py inspect` 只读采集，不写系统。所有命令都是固定 argv，不经过 shell；缺少工具时字段为 `null` 或空数组，不猜测值。

## 主要字段

| 区域 | 来源 | 说明 |
| --- | --- | --- |
| `host` | `/etc/os-release`、`uname`、DMI、`/proc/sys/kernel/random/boot_id` | 发行版、内核、架构、机型、虚拟化/容器 |
| `cpu` | `/proc/cpuinfo`、`/sys/devices/system/cpu/cpu*` | 型号、逻辑/物理核、P/E 核、调频驱动、governor、EPP、Intel/AMD pstate |
| `memory` | `/proc/meminfo`、`/proc/sys/vm`、`/sys/block/zram*` | 总量/可用/交换（MiB）、swappiness、脏页比例、THP、zram |
| `gpu` | `/sys/class/drm/card*`、`lspci -Dnn`、`glxinfo -B`、`nvidia-smi`、`vainfo`、`vulkaninfo --summary` | 显卡 PCI ID、驱动、Mesa、VA-API、Vulkan、当前显示输出 |
| `storage` | `/proc/mounts`、`lsblk -J`、`/sys/block/*/queue` | 根文件系统、设备、NVMe/SSD/HDD、I/O 调度器 |
| `power` | `/sys/class/power_supply`、`/sys/firmware/acpi/platform_profile`、gsettings、power-profiles-daemon、tuned | 电池、交流电、DDE 电源模式、平台 profile、温度 |
| `desktop` | `/usr/share/{x,wayland}-sessions`、环境变量、gsettings | X11/Wayland 会话、DDE schema、动画设置 |
| `network` | `/sys/class/net/*`、systemd units | Wi-Fi 是否存在、驱动、NetworkManager |
| `services` | `systemctl list-unit-files`、`list-units` | fstrim、oomd、irqbalance、thermald、电源守护、数据库单元 |
| `databases` | `/etc/postgresql/*/main/postgresql.conf`、`/etc/mysql`、`/etc/redis/redis.conf`、`sqlite3 --version` | 只读配置与单元状态，不连接数据库；MySQL 区分客户端目录与服务端二进制/服务单元、产品和版本 |
| `capabilities` | `os.geteuid`、`sudo -n true`、工具存在性 | 是否 root、免交互 sudo、systemd、gsettings、DDE |

## 分类

`classification` 是启发式摘要，不是硬件评分：

- `form_factor`：有电池为 `laptop`，否则 `desktop`。
- `cpu_class`：`intel-hybrid`、`intel`、`amd-hybrid`、`amd`，无法识别时为 `unknown`（不会默认当成 AMD）。混合核优先看 `topology/core_type`；没有时比较每核最大频率，容量相同则不把同构 CPU 误判为混合核。
- `gpu_class`：`intel`、`amd`、`nvidia`、`unknown`；多显卡时为 `hybrid-*`。
- `primary_gpu_class`：按 `boot_vga` 或第一张显卡判断实际输出 GPU；VA-API 和 GL 环境变量按它选择，避免混合显卡把独显驱动写成全局默认。
- `memory_class`：`low` < 8 GiB、`mid` ≤ 16 GiB、`high` > 16 GiB。
- `storage_class`：`nvme`、`ssd`、`hdd`、`unknown`。
- `power_source`：`ac`、`battery`、`unknown`。
- `display_width` / `display_refresh`：X11 下从 `xrandr` 当前模式读取；Wayland 或缺少 `xrandr` 时可能为空。

## 限制

- 探测不跑基准测试，不承诺“这个配置一定比默认快”。评分只用于排序候选方案。
- 虚拟机、容器、eGPU、NVIDIA Optimus/PRIME、AMD 双显卡的识别依赖内核和工具暴露的信息；未知时不要补造显卡或驱动。
- 温度传感器可能存在异常值；探测只保留 0–150°C 范围内的读数，仍不能替代真实散热测试。
- `glxinfo`、`vainfo`、`vulkaninfo`、`nvidia-smi` 是可选项。缺少它们时报告未验证，不自动安装。
- Deepin 的 `/usr`、`/etc` 可能由 overlay/ostree 管理；本技能只写 `/etc` 下的独立 drop-in，不修改镜像层或 GRUB 内核命令行。


## 桌面原生能力

`desktop_native` 使用 busctl 的 JSON 输出和 XML introspection 采集 Power1、Display1、Appearance、X11 WM/KWin 特效及 ConfigManager 的实际能力。包含每个活动输出的 Modes、CurrentMode、BestMode、亮度和缩放。旧 xrandr 摘要继续用于硬件评分；实际显示计划使用 DDE Modes，不以摘要替代可用模式枚举。Power1.Mode 是新后端运行态，旧 power.dde 字段保留为兼容配置读数，两者可能不同。

dconfig_resources 列出 installed 键与覆盖状态；只读资源不转成操作。安装了 Treeland 的资源不能说明当前会话使用 Treeland；未知 Wayland 合成器的专用设置保持不支持。详见 [desktop.md](desktop.md)。
