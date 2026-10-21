# org.deepin.dde.Search1 接口参考

检索调用方提供的字符串集合，支持中文拼音与模糊匹配。服务不扫描目录、不读取文件正文，也不建立系统文件全文索引。创建候选集合会写入当前用户的搜索缓存。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.deepin.dde.Search1` |
| Object path | `/org/deepin/dde/Search1` |
| Interface | `org.deepin.dde.Search1` |
| Bus | Session |

调用当前用户的会话服务，无需切换到 root。搜索标识来自创建集合的返回值，不是待搜索文件的校验和，也不能使用空内容 MD5 代替。创建方法返回后缓存写入仍可继续，立即搜索为空不一定表示没有匹配项。

## 创建候选集合

### NewSearchWithStrList

- **功能**：为传入字符串列表建立候选集合，加入原字符串及其拼音匹配形式；查询返回原字符串。
- **输入参数**：`list`（`as`）：候选字符串列表。
- **返回值**：`md5sum`（`s`）：集合的缓存标识；`ok`（`b`）：是否成功发起创建。
- **使用场景**：应用内选项、名称列表和启动项的搜索。

```bash
gdbus call --session \
  --dest org.deepin.dde.Search1 \
  --object-path /org/deepin/dde/Search1 \
  --method org.deepin.dde.Search1.NewSearchWithStrList \
  '["System Settings", "Terminal", "Calculator"]'
```

保存实际返回的集合标识为 `search_id`。`ok=true` 不表示异步缓存已经全部写完。

### NewSearchWithStrDict

- **功能**：为字符串映射建立候选集合，匹配字段包含字典值，中文键可参与拼音匹配；查询返回原字典键。
- **输入参数**：`dict`（`a{ss}`）：候选键值映射。
- **返回值**：`md5sum`（`s`）：集合的缓存标识；`ok`（`b`）：是否成功发起创建。
- **使用场景**：应用需要以显示名称匹配并取得稳定条目标识。

```bash
gdbus call --session \
  --dest org.deepin.dde.Search1 \
  --object-path /org/deepin/dde/Search1 \
  --method org.deepin.dde.Search1.NewSearchWithStrDict \
  '{"settings": "System Settings", "terminal": "Terminal"}'
```

## 查询候选集合

### SearchString

- **功能**：在已创建的集合中执行忽略大小写的模糊匹配，按匹配评分排列并去重。
- **输入参数**：`str`（`s`）：查询表达式；`md5sum`（`s`）：创建方法返回的集合标识。
- **返回值**：`as`：匹配的原字符串或原字典键。
- **使用场景**：应用内候选列表的搜索排序。

```bash
gdbus call --session \
  --dest org.deepin.dde.Search1 \
  --object-path /org/deepin/dde/Search1 \
  --method org.deepin.dde.Search1.SearchString \
  "term" "${search_id:?请使用候选集合创建方法返回的实际标识}"
```

### SearchStartWithString

- **功能**：对集合中的匹配字段执行忽略大小写的正则前缀匹配，去重后返回结果。
- **输入参数**：`str`（`s`）：正则表达式的前缀部分；`md5sum`（`s`）：实际集合标识。
- **返回值**：`as`：匹配的原字符串或原字典键。
- **使用场景**：只需前缀匹配的候选项筛选。

```bash
gdbus call --session \
  --dest org.deepin.dde.Search1 \
  --object-path /org/deepin/dde/Search1 \
  --method org.deepin.dde.Search1.SearchStartWithString \
  "term" "${search_id:?请使用候选集合创建方法返回的实际标识}"
```

查询文本会参与正则构造，纯文本调用方应转义正则特殊字符；不能把任意未经处理的表达式当成普通文件名查询。

## 完整调用示例

以下 Python 示例依赖 PyGObject，创建示例候选并在限定时间内等待缓存可查询，不修改系统设置：

```python
from gi.repository import Gio, GLib
import time

bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
service = "org.deepin.dde.Search1"
path = "/org/deepin/dde/Search1"

def call(method, signature, arguments):
    return bus.call_sync(service, path, service, method,
                         GLib.Variant(signature, arguments), None,
                         Gio.DBusCallFlags.NONE, 2000, None).unpack()

search_id, ok = call("NewSearchWithStrList", "(as)",
                     (["System Settings", "Terminal", "Calculator"],))
if not ok:
    raise RuntimeError("Cannot create candidate set")
deadline = time.monotonic() + 2
while True:
    results, = call("SearchString", "(ss)", ("Terminal", search_id))
    if results:
        print(results)
        break
    if time.monotonic() >= deadline:
        raise TimeoutError("Candidate cache is not ready")
    time.sleep(0.05)
```
