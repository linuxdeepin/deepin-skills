# org.deepin.dde.Pinyin1 接口参考

该接口提供中文拼音搜索能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Pinyin1` |
| Object path | `/org/deepin/dde/Pinyin1` |
| Interface | `org.deepin.dde.Pinyin1` |
| Bus | Session |

> **待核验声明**：本文档接口信息基于源码静态分析，未经运行时 D-Bus 内省验证，标记为待核验。

### 拼音查询方法

#### Query

查询单个汉字的拼音。

- **输入参数**: `s`（string, 类型 `s`）：汉字
- **返回值**: `s`（string）：拼音

```bash
gdbus call --session \
  --dest org.deepin.dde.Pinyin1 \
  --object-path /org/deepin/dde/Pinyin1 \
  --method org.deepin.dde.Pinyin1.Query "你好"
```

#### QueryList

查询多个汉字的拼音列表。

- **输入参数**: `s`（string, 类型 `s`）：汉字串
- **返回值**: `as`（string 数组）：拼音列表

```bash
gdbus call --session \
  --dest org.deepin.dde.Pinyin1 \
  --object-path /org/deepin/dde/Pinyin1 \
  --method org.deepin.dde.Pinyin1.QueryList "你好世界"
```

