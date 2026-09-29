# org.deepin.dde.Search1 接口参考

该接口提供系统搜索和搜索字典管理能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Search1` |
| Object path | `/org/deepin/dde/Search1` |
| Interface | `org.deepin.dde.Search1` |
| Bus | Session |
### 搜索方法

#### NewSearchWithStrDict

使用字符串字典创建搜索。

- **功能**：使用字符串字典创建搜索实例并返回搜索句柄。
- **触发条件**：当需要基于键值对字典进行文件搜索时调用。
- **使用场景**：文件搜索引擎初始化搜索实例。

- **输入参数**: `dict`（字典, 类型 `a{ss}`）：搜索字典
- **返回值**: `(s, b)`（结构体）：搜索句柄和是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.Search1 \
  --object-path /org/deepin/dde/Search1 \
  --method org.deepin.dde.Search1.NewSearchWithStrDict '{"key":"value"}'
```

#### NewSearchWithStrList

使用字符串列表创建搜索。

- **功能**：使用字符串列表创建搜索实例并返回搜索句柄。
- **触发条件**：当需要基于关键词列表进行文件搜索时调用。
- **使用场景**：文件搜索引擎初始化搜索实例。

- **输入参数**: `list`（string 数组, 类型 `as`）：搜索列表
- **返回值**: `(s, b)`（结构体）：搜索句柄和是否成功

```bash
gdbus call --session \
  --dest org.deepin.dde.Search1 \
  --object-path /org/deepin/dde/Search1 \
  --method org.deepin.dde.Search1.NewSearchWithStrList '["item1","item2"]'
```

#### SearchStartWithString

使用字符串开始搜索。

- **功能**：使用字符串开始搜索并返回搜索结果。
- **触发条件**：当需要基于单个关键词开始文件搜索时调用。
- **使用场景**：文件搜索开始搜索。

- **输入参数**: `str`（string, 类型 `s`）：搜索字符串；`md5sum`（string, 类型 `s`）：MD5 校验值
- **返回值**: `as`（string 数组）：搜索结果

```bash
gdbus call --session \
  --dest org.deepin.dde.Search1 \
  --object-path /org/deepin/dde/Search1 \
  --method org.deepin.dde.Search1.SearchStartWithString "keyword" "d41d8cd98f00b204e9800998ecf8427e"
```

#### SearchString

搜索字符串。

- **功能**：执行字符串搜索并返回匹配结果列表。
- **触发条件**：当需要执行一次完整搜索并获取结果时调用。
- **使用场景**：文件搜索执行搜索并返回结果。

- **输入参数**: `str`（string, 类型 `s`）：搜索字符串；`md5sum`（string, 类型 `s`）：MD5 校验值
- **返回值**: `as`（string 数组）：搜索结果

```bash
gdbus call --session \
  --dest org.deepin.dde.Search1 \
  --object-path /org/deepin/dde/Search1 \
  --method org.deepin.dde.Search1.SearchString "keyword" "d41d8cd98f00b204e9800998ecf8427e"
```
