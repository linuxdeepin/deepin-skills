# dde-appearance

dde-appearance 是 DDE 桌面环境的外观管理组件。通过 Session 总线提供当前用户桌面的外观设置（字体、主题、壁纸、光标、缩放、窗口圆角、不透明度）和窗口管理器工作区背景切换能力。

外观设置作用于当前用户的桌面；工作区与窗口操作针对当前窗口管理器。壁纸轮播和处理缓存由相应后端管理；Portal 的壁纸请求使用门户调用契约。外观日常设置使用公开外观接口，不使用 UOS ID 内部同步恢复协议。

制作主题包、校准图标视觉大小或安装自定义资源时，先读[主题自定义、安装与应用](theme-customization.md)；仅切换已有主题时直接读取下方接口参考。

## D-Bus 接口

### 外观设置

提供当前用户桌面的字体、主题、壁纸、光标、缩放、窗口圆角、不透明度的读写接口。

详见 [org.deepin.dde.Appearance1.md](dbus/org.deepin.dde.Appearance1.md)

### 窗口管理器

提供当前会话的工作区背景切换、装饰主题设置、多任务状态控制和窗口显示操作。

详见 [com.deepin.wm.md](dbus/com.deepin.wm.md)
