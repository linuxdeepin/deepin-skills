# org.desktopspec.MimeManager1 接口参考

该接口用于系统级 MIME 类型管理，管理所有应用的 MIME 关联，提供默认应用 MIME 类型设置能力。

## 接口信息

| 字段 | 值 |
|------|------|
| Service | `org.desktopspec.ApplicationManager1` |
| Object path | `/org/desktopspec/MimeManager1` |
| Interface | `org.desktopspec.MimeManager1` |
| Bus | Session |

### MIME 类型管理操作

#### queryDefaultApplication

查询指定内容或 MIME 类型的默认应用。

- **输入参数**: `content`（string, 类型 `s`）：文件绝对路径或 MIME 类型
- **返回值**: `mimeType`（string, 类型 `s`）：MIME 类型；`application`（object path, 类型 `o`）：默认应用对象路径

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/MimeManager1 \
  --method org.desktopspec.MimeManager1.queryDefaultApplication "text/plain"
```

#### setDefaultApplication

设置 MIME 类型的默认应用。

- **输入参数**: `defaultApps`（字典, 类型 `a{ss}`）：MIME 类型到应用 ID 的映射
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/MimeManager1 \
  --method org.desktopspec.MimeManager1.setDefaultApplication '{"text/plain":"org.deepin.editor"}'
```

#### unsetDefaultApplication

取消指定 MIME 类型的默认应用设置。

- **输入参数**: `mimeTypes`（string 数组, 类型 `as`）：MIME 类型列表
- **返回值**: 无

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/MimeManager1 \
  --method org.desktopspec.MimeManager1.unsetDefaultApplication "['text/plain']"
```

#### listApplications

列出指定 MIME 类型关联的所有应用及其属性。

- **输入参数**: `mimeType`（string, 类型 `s`）：MIME 类型
- **返回值**: `applications_and_properties`（字典, 类型 `a{oa{sa{sv}}}`）：应用对象路径到属性映射

```bash
gdbus call --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/MimeManager1 \
  --method org.desktopspec.MimeManager1.listApplications "text/plain"
```

### 信号

#### MimeInfoReloaded

MIME 信息重新加载时发出。

- **参数**: 无

```bash
gdbus monitor --session \
  --dest org.desktopspec.ApplicationManager1 \
  --object-path /org/desktopspec/MimeManager1
```

---
