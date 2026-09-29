# org.deepin.dde.Pinyin1 接口参考

该接口提供中文汉字转拼音查询能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Pinyin1` |
| Object path | `/org/deepin/dde/Pinyin1` |
| Interface | `org.deepin.dde.Pinyin1` |
| Bus | Session |

## 拼音查询方法

### Query

查询单个汉字字符串的拼音。

- **功能**: 将输入的汉字字符串转换为对应的拼音列表
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 输入法拼音提示、中文搜索排序、汉字注音显示

- **输入参数**:
  - `hans`（string, 类型 `s`）：汉字字符串
- **返回值**: `pinyin`（string 数组, 类型 `as`）：拼音列表

```bash
gdbus call --session \
  --dest org.deepin.dde.Pinyin1 \
  --object-path /org/deepin/dde/Pinyin1 \
  --method org.deepin.dde.Pinyin1.Query \
  "你好"
```

### QueryList

查询多个汉字字符串的拼音列表，返回 JSON 格式结果。

- **功能**: 批量查询多个汉字字符串的拼音，以 JSON 格式返回结果
- **触发条件**: 由应用程序通过 D-Bus 调用触发
- **使用场景**: 批量中文文本拼音转换，如通讯录排序、批量注音

- **输入参数**:
  - `hansList`（string 数组, 类型 `as`）：汉字字符串数组
- **返回值**: `jsonStr`（string, 类型 `s`）：JSON 格式的拼音结果（键为输入汉字，值为拼音数组）

```bash
gdbus call --session \
  --dest org.deepin.dde.Pinyin1 \
  --object-path /org/deepin/dde/Pinyin1 \
  --method org.deepin.dde.Pinyin1.QueryList \
  "['你好', '世界']"
```
