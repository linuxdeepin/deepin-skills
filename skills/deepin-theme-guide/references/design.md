# 图标与鼠标的设计流程

## 从风格要求到造型

先把用户的要求落到可绘制的特征：轮廓与材质、应用辨识方式、配色与明暗关系、鼠标尖端/热点。名称和 description 是元数据，不会自动改变图形。用户要求新的游戏、水墨、机械等造型时，需要选合适的基础系列并提供自绘 SVG；不能只改标题和颜色就宣称完成该风格。

生成器提供三套基础系列，支持继续重绘：

| icon.style / cursor.style | 图标 | 鼠标 |
| --- | --- | --- |
| crafted（默认） | 按功能区分色族；常用应用使用文件夹、球体、面板、唱片、购物袋等独立物体；其余使用统一底板 | 亮色主体、深色内轮廓、亮色外轮廓和小面积强调色 |
| ink | 墨色切角漆面、暖白符号、金色细边与朱砂印记 | 暖白主体、墨色轮廓、朱砂刃面 |
| neon | 深蓝底板、双色边缘、清晰亮色符号，减少会糊掉细节的光晕 | 亮白主体、深色轮廓、小面积青色强调 |

outline、solid 仍可显式选择，但不再是默认。内置图形是基础设计，不能承诺复刻品牌 Logo 或原版游戏美术。若用户偏好与这些系列不符，应画自定义素材，不把三个系列变成唯一可选风格。

## 先看代表稿，再扩展范围

先在独立目录生成代表稿，包含常用应用、一个未知应用、方向/电量/音量变化和鼠标状态。使用真实名称，避免字母标签充当应用设计。风格及效果已有授权时，模型可以自行检查、修订并继续；预览步骤不意味着必须再请求用户批准。

```bash
python3 "<技能目录>/scripts/theme_pack.py" create --spec /绝对路径/spec.json --output /绝对路径/theme-package --summary
python3 "<技能目录>/scripts/theme_pack.py" design-preview --package /绝对路径/theme-package --output /绝对路径/design-preview.png
```

预览输出必须位于包外，可选 .svg（无额外 Python 图像依赖）或 .png（需已有 rsvg-convert）。--names 可指定最多 32 个逗号分隔的名称；覆盖旧预览需 --force。明暗背景分别展示 16/24/48px 图标及 24/32/48px 光标，红点标明热点；脚本不会自动把 visual_verified 改为 true。

用图片查看工具看真实预览：辨识度、视觉重量、边缘与留白、明暗对比、状态含义、鼠标尖端与热点是否对齐。小尺寸应删去装饰，不能只把大图缩小。预览显示静态 SVG 源文件，光标二进制和实际切换还需独立运行时验证。缺少图片查看能力时报告未观察，不以文件大小、路径数量或测试通过替代视觉质量。

## 应用与系统图标分别处理

应用图标保留足够的辨识特征，必要时通过 icon.overrides 提供逐应用稿；系统 actions/status/symbolic 图标保持简洁的符号表达，不套大面积应用底板。箭头朝向、电量、信号、静音、充电等必须由图形区分，不能复用同一图形后改文件名。内置状态处理覆盖常用名称，不代表能识别基准主题中的全部私有状态。

```json
"icon": {
  "style": "crafted",
  "scope": "desktop",
  "design_policy": "custom-apps",
  "unknown": "preserve",
  "overrides": {
    "vendor-app": {
      "source": "/绝对路径/vendor-app.svg",
      "variants": {"16": "/绝对路径/vendor-16.svg", "24": "/绝对路径/vendor-24.svg"}
    }
  }
}
```

内置稿包含 16/24px 简化版本与 scalable 大稿。custom 的 variants 可省略，省略时复制 source；不能把复制后的版本报告为独立设计。label 仍支持显式的少量文字，默认不生成字母徽标；小尺寸不显示模板 label。

unknown=preserve（默认）对无法识别的名称优先复制本机指定 base_theme 中可校验的静态 SVG，记录来源、原路径与摘要，保留辨识度。没有兼容 SVG 时使用通用占位图并列出；unknown=placeholder 可显式禁用保留。保留素材不算原创重绘，完整换画风任务需要继续补画这些项。不要给几千个基准名称批量套模板后宣称品牌图标已全部设计；通常先完成 desktop 的真实使用范围，再按需要扩展 base-theme。分享生成包时应保留基准素材适用的来源与许可。

design-report.json 单列 generated、custom、preserved、placeholders 以及鼠标自定义状态，其 `icon_design` 检查实际应用引用。默认 `restyle-apps` 使原图和占位图保持待完成；`custom-apps` 还要求用自绘素材替换语义模板。上面的示例在每个应用引用补齐前仍是未完成稿。读取 `icon_design.pending` 可获得具体名称和 desktop ID，包括动作图标和绝对路径别名。类别素材只作用于已记录别名，精确名称优先。详见 [icons.md](icons.md)。

文件覆盖率、GTK/Qt 加载、设计覆盖率和实际视觉质量是彼此独立的结果。提供 SVG 不等于其外观符合要求的风格；在宣称视觉统一前，应检查代表稿和剩余批次。

## 鼠标可以逐状态设计

默认 15 个状态：left_ptr、hand1、text、watch、crosshair、fleur、sb_h_double_arrow、sb_v_double_arrow、bd_double_arrow、fd_double_arrow、not-allowed、help、progress、grab、grabbing，并提供常用别名。wait 和 progress 含义独立，不能把忙碌箭头直接当等待圆环。当前内置稿是静态，不声称支持动画。

```json
"cursor": {
  "style": "ink",
  "sizes": [24, 32, 48],
  "colors": {"fill": "#EEE8D7", "outline": "#161A21", "accent": "#BB4245"},
  "overrides": {
    "left_ptr": {"source": "/绝对路径/blade-arrow.svg", "hotspot": [4, 3]}
  }
}
```

colors 是鼠标专用颜色，不直接把系统的浅/深活动色当作填充与描边。自定义 source 必须是静态 SVG，viewBox="0 0 32 32"；hotspot 是同坐标系内的 [x,y]，范围 0≤x,y<32，编译到每档时缩放并检查边界。注意尖端、留白和外描边，别让热点落在看起来空白的位置。SVG 原形、热点和编译文件纳入包摘要及恢复流程。自绘的形状不会自动获得内置稿的双轮廓，需要在素材中自行处理。

静态 SVG 可使用 path、几何形状、渐变、内部 use、裁剪和受限滤镜；禁止脚本、事件、外部图片、字体或其他外部引用。不能为增加效果放宽到任意 SVG/HTML。运行时与平台边界见 [cursor.md](cursor.md)。
