# 图标生成、覆盖与实际命中

## 为什么旧主题只改变部分图标

旧生成器的 12 类模板只产生约 20 个名称。例如 `deepin-terminal` 被覆盖，`dde-file-manager`、`chatgpt` 可能完全没有新文件。`Inherits=bloom,hicolor` 会让缺失名称回退到原有资源，保持可用，但不会把旧图标改成新风格。DDE 读回新主题 ID 也不能证明应用实际加载了新文件。

`.desktop` 的 `Icon=/绝对路径/icon.png` 直接指定文件，不经过命名图标主题；应用内嵌图片、部分沙箱/玲珑私有资源、Qt/DTK 自己绘制的图标也可能独立于主题。不要把全部缺项都归因于缓存。

## 目标范围

| `icon.scope` | 扫描目标 | 用途 |
| --- | --- | --- |
| `applications` | XDG 有效应用启动器及声明的 Desktop Action 图标 | 仅补齐应用图标 |
| `desktop`（默认） | 应用 + 常用位置、状态、设备、MIME、动作名称 | 一般桌面主题 |
| `base-theme` | desktop + 指定基准主题目录中的全部 SVG/PNG/XPM 名称 | 用户要求覆盖当前完整图标主题时优先 |
| `explicit` | `names` 和 `overrides` 指定的名称 | 少量试样，不表示整套桌面 |

扫描顺序为 `$XDG_DATA_HOME/applications`，再按 `$XDG_DATA_DIRS` 的顺序。遵循同 ID 的用户覆盖、Hidden 掩盖、保留大小写；NoDisplay 工具也纳入，避免启动器之外的应用关联图标遗漏。嵌套 desktop 路径转为带连字符的 desktop ID。扫描不执行 Exec/TryExec；不依据当前菜单可见性删除目标，保守保留 OnlyShowIn 等条件项。

本来没有 Icon 的启动器没有可替换的命名引用，单列 entries_without_icon，不计入名称覆盖率的分母，也不阻止已有引用的完整覆盖；这不表示给这些启动器新增了图标。重复 Name/GenericName/Comment/Keywords 的翻译键使用最后值并记录 parse_warnings；重复分组或 Icon 等非翻译键仍报错。

`base-theme` 只枚举该主题本身，继承主题中的私有名称不自动递归加入；另行确认需要覆盖的基准范围。每包最多 20000 个名称，超出则分范围处理并如实说明。图标只支持安全文件名；不支持的引用和解析错误均列在报告中，不静默计为成功。

先扫描当前机器：

```bash
python3 "<技能目录>/scripts/theme_pack.py" icon-inventory --scope base-theme --base-theme bloom --output /绝对路径/icon-inventory.json
```

基准 ID 取自本机实际目录/catalog，不凭空假定 bloom 可用。输出包括应用数、目标名称数、绝对路径例外和扫描错误。完整清单留在本地 JSON；不必把所有启动器内容发送给模型。`--app-dir` 可重复指定目录，顺序决定优先级；指定后替代默认 XDG 应用目录。

## 生成与精细设计

独立图标规范示例：

```json
{
  "id": "neon-cyberpunk-icons-v2",
  "name": "Neon Cyberpunk Icons v2",
  "palette": {"light": "#00A9B8", "dark": "#FF2D95", "apply_accent": false},
  "icon": {
    "scope": "base-theme",
    "base_theme": "bloom",
    "inventory": "/绝对路径/icon-inventory.json",
    "style": "neon",
    "overrides": {
      "dde-file-manager": {"template": "folder"},
      "chatgpt": {"template": "assistant"},
      "vendor-app": {"source": "/绝对路径/原创vendor-app.svg"}
    }
  }
}
```

`inventory` 可省略，此时生成阶段直接扫描。使用已保存清单时，scope 必须匹配。新增应用或启动器变化后重新扫描并生成新 ID。`names` 兼容旧的基础类别（会展开别名），也支持准确的新名称；如果只给 names、不指定 scope，则保留旧的 explicit 语义。要全量生成应明确 scope 或完全省略 names。

`terminal`、`browser`、`settings` 等类别覆盖会展开到目标清单中已有的别名：`terminal` 覆盖 `utilities-terminal` 和 `deepin-terminal`；`browser` 覆盖 `web-browser`、`firefox`、`chromium` 和 `deepin-browser`；`settings` 覆盖 `preferences-system`、`dde-control-center` 和 `deepin-control-center`。其他旧类别按 theme_pack.py 的 `ICON_FILES` 展开。素材、模板、标签和小尺寸变体一起传播；精确名称覆盖始终优先，与键顺序无关。manifest 会记录 `override_key`；不做子串或猜测品牌映射。使用其他名称的自定义启动器需要其准确的清单键。

每个扫描到的名称都有自己的文件，不再依靠固定模板的少量别名覆盖。自动识别名称选择语义图形；无法识别的名称默认优先保留可校验的本机基准 SVG，并在 design-report.json/manifest 标记 preserved 与来源；无法保留时使用占位图，列为 `generic_names`。保留图不计为原创重绘；设计系列、默认无字母徽标、小尺寸独立稿和预览方法见 [design.md](design.md)。对关键应用逐个设计本地 SVG，通过 `overrides.source` 输入；它优先于模板。用户要求所有应用精细重绘时，应按清单分批提供自绘 SVG，不能用通用模板或保留素材的文件覆盖率替代设计完成度。模板可选 folder、terminal、browser、assistant、store、monitor 等；`label` 最多 4 个字符。

`icon.design_policy` 控制设计验收：

| 取值 | 视为完成的应用素材 | 待完成项 |
| --- | --- | --- |
| `restyle-apps`（默认） | 自绘 SVG 或已识别的语义风格模板 | 保留原图、占位图、缺失素材 |
| `custom-apps` | 通过 `overrides.source` 提供的自绘 SVG | 上述全部，加上内置模板 |

用户要求逐应用精细重绘，或所选内置风格无法表达要求的造型/材质时使用 `custom-apps`；内置风格已满足要求时用默认值。两种策略都按实际启动器引用统计，包括 Desktop Actions 和为绝对路径生成的别名，即使某引用与 places/status 常用名称重合。`explicit` 只检查选中的名称，不能证明全部应用覆盖。应用引用之外的基准主题额外名称仍保留在整体设计统计中，供评审。

`create` 与 `validate` 对未完成稿也可能成功：它们的 `ok` 只表示包完整性。检查重新计算的 `icon_design` 与 `design_complete`（也保存在 design-report.json）。`icon_design.pending` 列出准确名称、desktop ID、模板和原因：`preserved_original`、`placeholder`、`missing_asset`、`custom_source_required`。补齐后重新生成新 ID；仅把 `unknown` 设为 `placeholder` 不会完成设计。脚本只检查声明的素材类型，不检查视觉合规，需人工按目标风格检查自绘 SVG。

自绘 SVG 最大 1 MiB，支持静态几何形状、渐变、内部 use、裁剪及受限滤镜；禁止脚本、事件与外部 href/url。复杂轮廓先转 path。生成后会解析 SVG 和检查资源摘要，不执行 SVG 中代码。无论模板还是自绘，都须在实际小尺寸观察辨识度、字形、符号意义、亮暗背景及 symbolic 图标表现；名称齐全不等于产品级视觉质量。

```bash
python3 "<技能目录>/scripts/theme_pack.py" create --spec /绝对路径/icons-spec.json --output /绝对路径/icons-v2 --summary
python3 "<技能目录>/scripts/theme_pack.py" validate --package /绝对路径/icons-v2 --summary
python3 "<技能目录>/scripts/theme_pack.py" icon-audit --package /绝对路径/icons-v2 --output /绝对路径/icon-audit-staged.json
```

包内 `icon-inventory.json` 是分母，`icon-coverage.json` 是文件覆盖，`manifest.json` 保存所有名称和摘要。`icon-audit` 在独立进程中通过 GTK3 与 Qt6 查找 24/48/96 三档，逐项记录实际文件；GTK 命中其他主题为 fallback，找不到为 unresolved。Qt 的 qt_runtime 单独报告加载来源，runtime_verified 仅在两者通过时为真。`technical_scope_complete` 还要求当前启动器状态和例外已解析；`scope_complete` 同时要求技术范围与 `design_complete`。复制原图即使能在新主题内命中，也可能通过运行时加载但不满足设计覆盖。旧包没有 design_policy 时按 restyle-apps 审计，其完整性和恢复记录仍然有效。待安装包只改变该辅助进程的查找路径，不激活桌面。缺少 GI/Gtk3 时 available=false，不能当作已验证；文件生成仍可用。

未处理绝对路径例外时，audit 返回 scope_complete=false/退出码 2；这是待处理结果，不是生成失败。GTK 和 Qt 分别验证；任一缺失不能宣称两者均通过。Qt 验证使用已有 g++、pkg-config 与 Qt6Gui 开发文件，不自动安装。两种查找验证仍不能代表应用缓存、沙箱或视觉均已验证。

## 绝对路径例外与激活

```bash
python3 "<技能目录>/scripts/theme_pack.py" install --package /绝对路径/icons-v2
python3 "<技能目录>/scripts/theme_pack.py" install --package /绝对路径/icons-v2 --execute
python3 "<技能目录>/scripts/theme_pack.py" activate --id neon-cyberpunk-icons-v2 --components icon --launcher-overrides
python3 "<技能目录>/scripts/theme_pack.py" activate --id neon-cyberpunk-icons-v2 --components icon --launcher-overrides --execute
python3 "<技能目录>/scripts/theme_pack.py" verify --id neon-cyberpunk-icons-v2 --components icon
python3 "<技能目录>/scripts/theme_pack.py" icon-audit --id neon-cyberpunk-icons-v2 --output /绝对路径/icon-audit-installed.json
```

预览展示 `launcher_overrides.operations` 中 desktop ID、原/新 Icon 值及创建/修改类型；仅在用户授权覆盖这些图标时执行。系统启动器在用户 applications 目录产生同 ID 副本；已有用户启动器只更改 Icon 键，包括声明的动作。Exec 字段原样保留、不执行，系统文件不修改。图标目录和启动器覆盖目录须位于当前 HOME；自定义 XDG_DATA_HOME 也遵守此限制。

每次写入先记录状态，失败恢复。恢复新建副本时，只有文件全文仍与本次写入相同才删除；已有文件逐 Icon 键恢复，保留其他手动编辑。遇到冲突保留当前值并报告 needs_attention。用户之后安装/升级应用可能使覆盖副本滞后，恢复或重新生成时关注原启动器变化，不长期盲目保留副本。

图标例外和待完成的应用设计默认都会在写入设置前阻止“完整”激活，包括选择了启动器覆盖的情形。用户明确接受后可加 `--allow-partial-icons`，但 scope_complete 仍为 false。不要为了让命令通过自行开启此标志。写入后查找失败或无运行时能力时，报告 applied_pending_runtime 并保留恢复点。范围不完整时，`verify` 与 `icon-audit` 即使 runtime_verified=true 也返回 ok=false/退出码 2。

## 只补齐旧包的图标

旧包没有清单时不能证明全量覆盖，使用新版生成新 ID，不覆盖原目录。换一整套主题时直接激活新包：重叠的图标组件（含绝对路径启动器覆盖）由新记录接管，旧记录归档为 `state=superseded`，其 change ID 仍可恢复到更早的图标基线。只有确实想回到旧包的图标时才先恢复旧记录：

```bash
python3 "<技能目录>/scripts/theme_pack.py" rollback --change-id change-旧包真实ID --components icon
python3 "<技能目录>/scripts/theme_pack.py" rollback --change-id change-旧包真实ID --components icon --execute
```

接管时旧覆盖副本必须仍与记录的 `after_hash` 一致；被手动修改的副本不会被静默覆盖。旧包的壁纸、光标、活动色和屏保继续保留，各自的恢复点不变。旧记录只恢复完部分组件时 state=applied，剩余组件恢复后才归档。新图标包也有独立 change ID；恢复新包时回到其执行前的图标值。

验收报告至少包含：scope 与目标数量、文件覆盖率、实际 GTK/Qt 命中数/查找数、fallback/unresolved、绝对路径处理数量、generic_names 数量、视觉观察范围和真实 change ID。不要用“主题 ID 已读回”代替这些结果，也不要为刷新图标自动注销或重启应用。

规范依据：[Freedesktop Icon Theme Specification](https://specifications.freedesktop.org/icon-theme-spec/latest/)、[Desktop Entry Icon key](https://specifications.freedesktop.org/desktop-entry-spec/latest/recognized-keys.html)。
