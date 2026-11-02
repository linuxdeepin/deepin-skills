---
name: deepin-font-manager
description: 提供面向最终用户的字体管理器中的一个或多个字体文件安装接口
Categories:
  - Application
---

# 字体管理器

提供面向最终用户的字体文件安装接口，不涉及开发库字体管理接口。

## 执行声明

> 分类规则：第三项只描述调用裸 D-Bus 前的服务注册前置条件，不等同于必须人工打开窗口；如果 deepin-tools 会自动拉起服务，会单独注明。第四项只列出 D-Bus 方法本身会打开、激活或进入交互界面的 action。

- 一步完成：无；`install` 返回只表示安装请求已提交，必须再确认用户完成安装并用 `fc-scan` 或 `fc-list` 校验字体文件。
- 需呼出界面并人工操作：`install` 可能弹出字体安装确认窗口；用户必须确认后，安装结果才可判定。
- 需先启动应用后 D-Bus 才存在：先用 `ll-cli list` 检查 `org.deepin.fontmanager`，必要时在当前图形会话执行 `ll-cli run org.deepin.fontmanager`，等待 `com.deepin.FontManager` 注册后再调用；不要求 Agent 人工打开字体管理器界面。
- 调用 D-Bus 直接呼出界面：无；当前接口未声明会打开字体管理器窗口。

## D-Bus 接口
接口信息：
- Bus：`session`
- Service：`com.deepin.FontManager`
- Object path：`/com/deepin/FontManager`
- Interface：`com.deepin.FontManager`

### install

安装一个或多个字体文件。安装请求通常写入当前用户目录 `~/.local/share/fonts/<Family>/`；调用后应使用 `fc-scan` 或 `fc-list` 校验，已存在的同 family/同内容字体可能跳过安装但仍返回成功。


执行说明：
- 分类：需呼出界面并人工操作；调用返回只表示安装请求已提交。
- 前置：先确认本 Skill 声明的 D-Bus 服务已注册；玲珑应用先完成启动与会话总线就绪检查。
- 完成判据：用户确认安装后，`~/.local/share/fonts/<Family>/` 中出现字体文件，并通过 `fc-scan` 或 `fc-list` 校验。

参数：
- `fonts`（array of string）：示例值 `$HOME/Downloads/NotoSansCJK-Regular.ttc`

接口：
- Method：`installFonts`

用例：
```bash
dbus-send --session --print-reply --dest=com.deepin.FontManager /com/deepin/FontManager com.deepin.FontManager.installFonts array:string:$HOME/Downloads/NotoSansCJK-Regular.ttc
```
