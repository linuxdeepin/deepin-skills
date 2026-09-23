# org.deepin.dde.Pinyin1 接口参考

该接口提供中文汉字到拼音的查询能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Pinyin1` |
| Object path | `/org/deepin/dde/Pinyin1` |
| Interface | `org.deepin.dde.Pinyin1` |
| Bus | Session |


### 拼音查询方法

#### Query

查询单个汉字或词语的拼音列表。

- **输入参数**: `hans`（string, 类型 `s`）：汉字
- **返回值**: `pinyin`（string 数组, 类型 `as`）：拼音列表

```bash
gdbus call --session \
  --dest org.deepin.dde.Pinyin1 \
  --object-path /org/deepin/dde/Pinyin1 \
  --method org.deepin.dde.Pinyin1.Query "重"
```

#### QueryList

查询多个汉字的拼音，返回 JSON 格式数据。

- **输入参数**: `hansList`（string 数组, 类型 `as`）：汉字列表
- **返回值**: `jsonStr`（string, 类型 `s`）：JSON 格式的拼音查询结果

```bash
gdbus call --session \
  --dest org.deepin.dde.Pinyin1 \
  --object-path /org/deepin/dde/Pinyin1 \
  --method org.deepin.dde.Pinyin1.QueryList \
  "['重', '好']"
```

---
