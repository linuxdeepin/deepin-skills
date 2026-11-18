# 新主题包工作流

## 设计规范

先让模型把自然语言偏好收敛为 JSON，再交给本地生成器。推荐字段：

```json
{
  "id": "aurora-blue",
  "name": "Aurora Blue",
  "description": "低饱和蓝色、清晰轮廓",
  "required_components": ["wallpaper", "icon", "cursor", "screensaver"],
  "palette": {"light": "#406A91", "dark": "#79A7D2"},
  "icon": {"style": "crafted", "scope": "desktop", "unknown": "preserve"},
  "cursor": {"style": "crafted", "size": 32, "sizes": [24, 32, 48]},
  "wallpaper": "/home/用户/Pictures/aurora.png",
  "screensaver": {"images": ["/home/用户/Pictures/aurora-1.jpg", "/home/用户/Pictures/aurora-2.jpg"], "interval": 30, "play_mode": 0, "activate": false}
}
```

`id` 是安装目录和 DDE 主题 ID，只允许小写字母、数字和连字符。`palette` 的两个颜色会映射为新 DDE 外观接口的浅色/深色活动色。省略组件就不生成、不安装、不激活。图标默认扫描实际应用与常用桌面名称；`scope=base-theme` 可进一步扫描指定基准主题的全部图标名。精确名称、清单、语义模板及逐应用自绘 SVG 见 [icons.md](icons.md)。`cursor.states` 从受支持的基础状态中选择，必须包含 left_ptr。`required_components` 可列出用户明确要求的组件，缺项时拒绝生成；整套任务应填写完整清单。

只想给生成资源配色而不修改系统活动色时，在 `palette` 中加 `"apply_accent": false`。图标只给 `names` 而不指定 scope 时采用 explicit 小范围模式；省略 names 则默认 desktop。光标省略 states 会生成全部基础状态。省略整个 icon 或 cursor 则不生成该组件。`cursor.size` 是基础名义尺寸，`cursor.sizes` 指定多档输出，默认包含 24/32/48 及基础尺寸；不改变系统当前的光标显示尺寸。`cursor.compiler` 默认 auto，也可指定 builtin 或 xcursorgen。`screensaver.activate` 仅是意图记录，实际激活始终需要命令中的 `--screensaver`。

`icon.design_policy` 默认为 `restyle-apps`：应用原图和占位图不计为已完成的风格工作。逐应用精细重绘时选 `custom-apps`，此时每个实际引用都需要 `overrides.source`。草稿生成和完整性校验仍可用，但待完成设计会阻止完整激活。查看 create/validate 或 icon-audit 重新计算的 `icon_design.pending`，补齐后重新生成。精确应用名称覆盖优先于已记录类别别名。策略细节与范围限制见 [icons.md](icons.md)。

设计时应先确定：背景图中图标的可见区域、图标轮廓粗细、光标的热点和最小可见尺寸、活动色在浅色和深色界面的对比度、屏保轮播速度。模型可以提出建议，但不能声称已经看过没有提供的图片；没有视觉输入时，只能根据文件和配置描述。

## 生成

```bash
python3 "<技能目录>/scripts/theme_pack.py" create \
  --spec /绝对路径/theme-spec.json \
  --output /绝对路径/aurora-blue-theme
```

生成器会创建：

```text
aurora-blue-theme/
├── manifest.json
├── palette.json
├── icon-inventory.json + icon-coverage.json # 如果生成图标
├── design-report.json                 # 素材来源与视觉待评审项
├── icons/aurora-blue/index.theme + scalable/*/*.svg + 16/*/*.svg + 24/*/*.svg
├── cursors/aurora-blue/index.theme + cursor.theme + source/*.svg + *.conf
├── cursors/aurora-blue/cursors/*       # 编译器齐全时
├── wallpapers/原名-内容摘要.png         # 如果规范提供
└── screensaver/images + config.json    # 如果规范提供
```

它生成的是可审阅的、用户级的独立包。图标按目标清单逐名生成，默认 crafted；ink、neon 提供其他基础系列，自绘 SVG 可逐项替代。未知名称优先保留可校验的基准 SVG，无法保留时标注占位图，不自动加字母。造型、自定义稿和预览验收见 [design.md](design.md)。`bloom,hicolor` 仍提供清单外的回退，但不计为新主题命中。生成后运行 `icon-audit`，绝对路径引用需显式用户级覆盖，否则默认阻止完整图标激活。光标 SVG 需要 `rsvg-convert` 转 PNG，再由 `xcursorgen` 或内置编译器生成 Xcursor。缺少光栅化工具时会保留源文件，并报告光标未编译；required_components 要求 cursor 时会拒绝未编译交付。缺少 xcursorgen 本身不再阻塞生成。

没有现成图片也可试跑内置规范：

```bash
python3 "<技能目录>/scripts/theme_pack.py" doctor
python3 "<技能目录>/scripts/theme_pack.py" create --spec "<技能目录>/assets/aurora-blue.json" --output /绝对路径/aurora-blue-theme
```

`create --force` 只允许替换带本生成器 manifest 的输出目录；它会删除旧输出，不能用于覆盖安装目录或保留了手工修改的目录。各文件的 SHA-256 记录在 manifest 的 `files` 中；手工改动包内文件后，校验会拒绝安装，应用修改请重新调整设计规范并生成新包。

生成器会复制用户明确指定的本地图片，并记录摘要。它不会联网下载素材，不会把 URL 当作本地文件，不会把模型输出的任意路径或 shell 片段直接执行。

## 校验和安装

```bash
python3 "<技能目录>/scripts/theme_pack.py" validate --package /绝对路径/aurora-blue-theme
python3 "<技能目录>/scripts/theme_pack.py" install --package /绝对路径/aurora-blue-theme
python3 "<技能目录>/scripts/theme_pack.py" install --package /绝对路径/aurora-blue-theme --execute
```

校验会拒绝符号链接、路径穿越、超大文件、摘要不匹配、缺少 `index.theme` 的图标主题、缺少 Xcursor 文件的已编译光标组件和缺少图片的屏保组件。安装目标是当前用户：

- 图标：`${XDG_DATA_HOME:-~/.local/share}/icons/<id>`（须位于当前 HOME）。
- 有编译光标时，两处均安装完整的图标/光标资源：`${XDG_DATA_HOME:-~/.local/share}/icons/<id>` 与 `~/.icons/<id>`；index.theme 一致，另有 cursor.theme。
- 整体主题卡片与封面：`${XDG_CONFIG_HOME:-~/.config}/dde-appearance/deepin-themes/<id>`。
- 壁纸通过系统服务导入自定义列表，使用服务返回的路径，所有权与摘要写入安装记录。包内记录图片尺寸；带网络来源时同时保存 `wallpapers/*.source.json` 与 manifest 摘要。获取与校验见 [wallpaper.md](wallpaper.md)。
- 完整主题包（含壁纸、屏保图片和 manifest）：`~/.local/share/uos-theme-personalize/themes/<id>`。
- 安装记录：`${XDG_STATE_HOME:-~/.local/state}/uos-theme-personalize/packages/`。

安装不会覆盖同名目录；换用新的 `id`，或先卸载未激活的旧包。它不需要 root，不写 `/usr/share/icons`、`/usr/share/themes` 或系统包数据库；原生壁纸服务负责其自定义缓存。安装会等候 DDE 目录扫描，使用 `desktop-status --id` 验证列表。完整行为、Gio/Qt 依赖、离线选项与卸载边界见 [control-center.md](control-center.md)。

安装后不再依赖原始生成目录，移动原始目录不影响已安装的壁纸和屏保。激活和卸载前会复核安装资源；若用户新增或修改了其中的文件，会保留文件并拒绝继续，以免误覆盖或删除。

## 激活

```bash
python3 "<技能目录>/scripts/theme_pack.py" activate --id aurora-blue
python3 "<技能目录>/scripts/theme_pack.py" activate --id aurora-blue --screensaver
python3 "<技能目录>/scripts/theme_pack.py" activate --id aurora-blue --screensaver --execute
```

激活预览列出原值、目标值和屏保配置。执行时，脚本直接写入 DDE 外观接口；先确认 desktop-status 的列表已就绪，再激活并检查实时加载；只有属性读回不足以证明点击切换生效。屏保使用 `dde-dconfig` 配置 Deepin 的 `deepin-custom-screensaver`：图片路径、间隔、播放模式和当前屏保名称都记录在变更中。目标系统缺少 `dde-dconfig`、自定义屏保组件或对应配置时，会阻止屏保项而不会修改其他项。

激活后的 `change-<16位十六进制>` 是恢复所需的唯一 ID。成功、失败和冲突状态均写到用户状态目录。只有激活后确认恢复，才可：

```bash
python3 "<技能目录>/scripts/theme_pack.py" rollback --change-id change-真实ID --execute
python3 "<技能目录>/scripts/theme_pack.py" uninstall --id aurora-blue --execute
```

不同包的非重叠组件允许分别保留恢复点，适合整套主题安装后补做光标。`activate --components cursor` 只选择鼠标；加 `--cursor-sync` 会预览和记录已有 DDE 光标配置键及 X11 资源同步。重复激活同一主题包，或存在 `applying`/`needs_attention` 等未完成记录时会拒绝写入。与已应用的旧记录组件重叠时不再要求先回滚：新激活直接接管，旧记录归档为 `change-<ID>.json` 且 `state=superseded`，其 change ID 仍可恢复到更早的基线。预览的 `supersedes` 列出被接管的记录，新记录的 `before` 就是切换前的值。

绝对路径启动器覆盖同样由新激活接管：旧覆盖副本内容经 `after_hash` 校验后作为本次计划的基线，不再因“出现新的用户启动器覆盖”或“应用清单变化”被拦下，也不需要重新生成主题包。若副本已被手动修改或不属于任何记录，仍会保留现值并报错。完整流程、`verify --id ... --observe-seconds 20` 和配置同步边界见 [cursor.md](cursor.md)。

补齐图标使用 `activate --components icon`；存在绝对路径启动器时先预览 `--launcher-overrides`。只有想回到旧包的图标时才需要 `rollback --components icon`；升级或换主题可直接激活新包。`verify --components icon` 同时检查 DDE 值、GTK/Qt 实际来源、应用清单变化和覆盖例外。`--summary` 可省略大批文件/查找明细，完整清单保存在包或变更记录中。详见 [icons.md](icons.md)。

恢复绑定原登录会话，读回 DDE 接口并检查冲突。光标同步、屏保冲突或恢复失败都会使整体结果为 `needs_attention`。若用户将冲突项调整回记录中的原值，可重新 rollback；不要修改状态文件绕过检查。

## 动态屏保边界

本包支持 Deepin 已安装的图片轮播屏保。它不把 SVG、HTML、JavaScript 或模型生成的可执行文件注册成屏保程序，也不自动编译或安装动态渲染器。要制作粒子、时钟、视频或实时数据屏保，需要单独开发符合目标版本屏保接口的受信任程序、签名/打包和资源限额策略。
