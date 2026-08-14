# Eval: v20 1070 DConfig/DCI 与缓存

## 任务

为 v20 1070 应用用 C++ 读取 DConfig，并用 `DDciIconPlayer` 播放图标动画；同时
说明用户配置的缓存位置和与 v25 的差别。

## 期望输出

1. 使用 DConfig 或 DCI 接口前，先检查目标 v20 1070 开发包实际发布且由编译器
   使用的公共头文件，不根据版本印象列出允许或禁止的方法、类或控件。
2. 只使用公共头文件中存在的 DConfig/DCI 声明，并确认 DCI 资源已安装。
3. v20 daemon 由 `dde-app-services` 提供，以 root 运行且不设置
   `StateDirectory`，用户缓存为用户家目录下 `.config/dsg/configs/...`。
4. v25 daemon 使用 `deepin-daemon` 与 `StateDirectory=dde-dconfig-daemon`，缓存
   根通常是 `/var/lib/dde-dconfig-daemon/.config`。

## 验证要点

- [ ] 以目标 v20 1070 发布的公共头文件确认 DConfig/DCI 接口
- [ ] 不维护单个接口或控件的 v20/v25 可用性清单
- [ ] 指出 daemon 属于 `dde-app-services`
- [ ] 正确区分 v20/v25 daemon 用户和缓存路径
