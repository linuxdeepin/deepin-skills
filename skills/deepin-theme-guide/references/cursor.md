# 光标生成、运行时诊断与恢复

## 编译与验证

缺少 `xcursorgen` 时，生成器会使用内置写入器，不安装依赖，也不让模型临时拼出另一个编译器。仍需要 `rsvg-convert` 将固定 SVG 模板转成 PNG。`cursor.compiler` 可用 `auto`、`builtin`、`xcursorgen`，默认 `auto`；强制指定的外部编译器缺失时会报错。

`cursor.sizes` 可以指定 1–8 档 16–128 的尺寸，默认包含 24、32、48 和 `cursor.size`。箭头热点以 32 像素图的 `(4,3)` 为基准，手型以 `(14,3)` 为基准，其他模板居中；progress/help 使用箭头尖端，每档独立缩放热点。自定义热点通过 overrides 输入。默认生成 15 种状态及常用别名，未覆盖的应用私有状态仍可能继承 bloom。支持 crafted、ink、neon 以及独立鼠标颜色；逐状态 SVG 与热点输入见 [design.md](design.md)。

内置解码器只接受有界、不交错、8 位的 PNG，处理 PNG 五种行过滤器；检查 CRC、解压长度和调色板。写入的是标准小端 Xcursor 图像块：`0xfffd0002`、尺寸、热点、延迟和预乘 alpha 的 ARGB 像素数组。PNG 是中间素材，不能直接塞进这种图像块。这是格式约定，不能描述为“这台机器的 libXcursor 特有缺陷”。

生成时检查每档结构，并在存在 libXcursor 时逐档加载。安装后按主题名和状态名重新加载，将尺寸、热点与像素摘要和该包的实际文件对比，以识别静默回退到别的主题。文件存在、`Xcur` 四字节魔数正确或返回了一个非空光标都不足以证明本包被使用。

安装布局、cursor.theme 与控制中心点击切换路径见 [control-center.md](control-center.md)。正常安装后使用原生切换，无需先做 --cursor-sync。

## 只读诊断

```bash
python3 "<技能目录>/scripts/cursor_runtime.py" --theme "真实主题ID" --cursor-dir "/绝对路径/.icons/真实主题ID" --observe-seconds 20
python3 "<技能目录>/scripts/theme_pack.py" verify --id "已安装包ID" --components cursor --observe-seconds 20
```

第二条命令专门验证主题包光标；其他组件继续看激活记录中的读回结果。`--observe-seconds` 为 0–30 秒，默认单次采样。观察窗口内有一次错误或不一致就报告未通过；20 秒稳定也不能证明以后永不变化。

诊断比较：

| 证据 | 能说明什么 |
| --- | --- |
| DDE `CursorTheme` | 外观接口的读回值 |
| 实时 XSettings Gtk/CursorThemeName 与 WM cursorTheme | X11 原生切换的实际传播值，和 DDE 值共同验收 |
| 已有 DDE GSettings `cursor-theme` | legacy_layers；可能是旧 schema，不单独决定实时切换是否成功 |
| 用户 kcminputrc / custom/index.theme 中已有光标键 | 潜在持久配置层的当前值，不能单独证明谁在覆盖它 |
| X11 `Xcursor.theme` | 当前 X 资源默认值；不是所有应用唯一的设置源 |
| 按名加载与包内像素摘要一致 | 新加载确实命中了本包资源 |
| 用户或实际桌面观察 | 被观察窗口和交互中的视觉效果 |

X11 原生 DDE 会话的 `configuration_consistent` 检查 DDE、实时 XSettings 和 WM；旧配置单列 legacy_layers。其他会话保留配置采样，不能外推成 X11 热更新证明。`configuration_consistent` 和 `named_lookup_matches` 独立报告，`visual_confirmation` 默认是 `not_observed`。GTK 可在收到设置变化后更新受支持的光标；自定义光标、其他工具包和特定应用可能有自己的缓存。不要笼统声称“X11 的所有已有进程都不能热更新”。

## 补齐已有整套主题中的鼠标

优先创建独立光标包，不修改已安装包的 manifest、文件摘要或安装记录：

```bash
python3 "<技能目录>/scripts/theme_pack.py" create --spec "<技能目录>/assets/neon-cyberpunk-cursor.json" --output "/绝对路径/neon-cursor-v2"
python3 "<技能目录>/scripts/theme_pack.py" install --package "/绝对路径/neon-cursor-v2"
python3 "<技能目录>/scripts/theme_pack.py" install --package "/绝对路径/neon-cursor-v2" --execute
python3 "<技能目录>/scripts/theme_pack.py" activate --id neon-cyberpunk-cursor-v2 --components cursor
```

预览包含 DDE 操作；只有另加 --cursor-sync 才生成 `cursor_sync.operations`。`--components cursor` 不改壁纸、图标和活动色；独立组件变更可与之前已成功的非重叠组件共存。同包重复激活或存在未完成变更时会拒绝写入；与旧记录组件重叠时由新激活接管，旧 change ID 仍可恢复到更早基线。用户已有授权覆盖同步范围后，可执行同一激活命令并加 `--execute`，随后 verify。

## 同步范围与恢复

`--cursor-sync` 只处理探测到的 DDE 光标键、已有的 `[Mouse] cursorTheme`、已有 custom/index.theme 的 DefaultTheme/DarkTheme 中 CursorTheme，以及 X11 当前 X 资源中的 `Xcursor.theme`。不创建未知 schema 或配置文件，不把这些位置视为所有 UOS 版本的统一真相。Wayland 跳过 xrdb；不会修改 XCURSOR_THEME 环境变量、锁屏策略或所有应用的私有配置。

每次键写入前保存原值和 started 状态，写入后读回。DDE 自身已把键更新到目标值时，也会保留原值用于恢复。恢复先处理 DDE，再恢复同步键；当前值既不是原值也不是本次目标值时保留并报告冲突。原 X 资源键不存在时，会基于当时的其他资源移除本次添加的键；不会用旧的整份资源覆盖新值。配置文本采用逐键替换，保留其他字段与文件权限。

激活后的 `applied_pending_runtime` 是已写入但未完成运行时验证，`ok=false` 不等于“完全没改”。状态记录仍用于 rollback。恢复某个同步键失败或冲突会保留 active 记录并返回 `needs_attention`。不要为刷效果反复改写其他配置或自动注销。

旧版本在技能之外修改的配置不会因升级而自动进入回滚记录。不得硬编码 bloom、bloom-dark、hazy-color 作为恢复值，也不要拿旧备份覆盖之后产生的其他设置。须分别核实旧备份与原记录，按用户要求制定独立修复方案。

## 官方依据

- [X.Org libXcursor 源码发布包](https://www.x.org/releases/individual/lib/libXcursor-1.2.3.tar.xz)：`include/X11/Xcursor/Xcursor.h` 定义图像块和 ARGB 像素，`src/file.c` 实现加载与写入。
- [GTK 3 X11 光标主题实现](https://github.com/GNOME/gtk/blob/gtk-3-24/gdk/x11/gdkcursor-x11.c)：`gdk_x11_display_set_cursor_theme` 更新可支持的已有缓存光标。
- [GTK 设置到光标主题的传递](https://github.com/GNOME/gtk/blob/gtk-3-24/gtk/gtksettings.c)：`settings_update_cursor_theme` 将设置传给 GDK。
