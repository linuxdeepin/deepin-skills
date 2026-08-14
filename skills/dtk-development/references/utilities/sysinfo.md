# DSysInfo 系统信息

## 1. 概述与适用场景

`DSysInfo`（dtkcore）提供运行时系统信息查询。主要用于判断 UOS 版本和系统类型，实现差异化功能。

**适用场景：**
- 根据 UOS 版本启用/禁用功能
- 判断桌面/服务器类型
- 获取系统版本号
- 区分社区版/专业版

## 2. 枚举

### 2.1 ProductType

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `UnknownType` | 未知 |
| 1 | `Deepin` | Deepin |
| 2 | `ArchLinux` | Arch Linux |
| 3 | `CentOS` | CentOS |
| 4 | `Debian` | Debian |
| 5 | `Fedora` | Fedora |
| 6 | `LinuxMint` | Linux Mint |
| 7 | `Manjaro` | Manjaro |
| 8 | `openSUSE` | openSUSE |
| 9 | `SailfishOS` | Sailfish OS |
| 10 | `Ubuntu` | Ubuntu |
| 11 | `Uos` | UOS |
| 12 | `Gentoo` | Gentoo |
| 13 | `NixOS` | NixOS |

### 2.2 DeepinType

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `UnknownDeepin` | 未知 |
| 1 | `DeepinDesktop` | 桌面版 |
| 2 | `DeepinProfessional` | 专业版 |
| 3 | `DeepinServer` | 服务器版 |
| 4 | `DeepinPersonal` | 个人版 |
| 5 | `DeepinMilitary` | 军工版 |

### 2.3 UosType

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `UosTypeUnknown` | 未知 |
| 1 | `UosDesktop` | 桌面 |
| 2 | `UosServer` | 服务器 |
| 3 | `UosDevice` | 设备 |
| 4 | `UosSmart` | 智能终端 |

### 2.4 UosEdition

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `UosEditionUnknown` | 未知 |
| 1 | `UosProfessional` | 专业版 |
| 2 | `UosHome` | 家庭版 |
| 3 | `UosCommunity` | 社区版 |
| 4 | `UosMilitary` | 军工版 |
| 5 | `UosEnterprise` | 企业版 |
| 6 | `UosEnterpriseC` | 企业C版 |
| 7 | `UosEuler` | 欧拉版 |
| 8 | `UosMilitaryS` | 军工服务器版 |
| 9 | `UosDeviceEdition` | 设备版 |
| 10 | `UosEducation` | 教育版 |
| 11 | `UosDefense` | 国防版 |

### 2.5 OrgType

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `Distribution` | 发行版自身 |
| 1 | `Distributor` | 发行商 |
| 2 | `Manufacturer` | 制造商 |

### 2.6 LogoType

| 值 | 名称 | 说明 |
|----|------|------|
| 0 | `Normal` | 普通 |
| 1 | `Light` | 浅色 |
| 2 | `Symbolic` | 象征性 |
| 3 | `Transparent` | 透明 |

## 3. 核心 API（全部静态方法）

### 3.1 系统判断

```cpp
#include <DSysInfo>

// 是否 Deepin/UOS
bool deepin = DSysInfo::isDeepin();

// 是否运行在 DDE 桌面
bool dde = DSysInfo::isDDE();

// 是否社区版
bool community = DSysInfo::isCommunityEdition();
```

### 3.2 版本查询

```cpp
// Deepin 类型
DSysInfo::DeepinType dtype = DSysInfo::deepinType();

// UOS 类型和版本
DSysInfo::UosType utype = DSysInfo::uosType();
DSysInfo::UosEdition edition = DSysInfo::uosEditionType();

// 版本号
QString major = DSysInfo::majorVersion();    // "20", "23"
QString minor = DSysInfo::minorVersion();
QString build = DSysInfo::buildVersion();
QString sp = DSysInfo::spVersion();           // "SP1" 等
```

`majorVersion()` 和 `minorVersion()` 按 Desktop Entry/INI 语义读取 `/etc/os-version` 的 `[Version]` 节中的 `MajorVersion`、`MinorVersion`。在 `dtk-development` 中，任务未明确目标系统时使用这两个字段判断 v20/v25；`/etc/os-release` 的 `VERSION_ID` 对应 `productVersion()`，不替代这里的判断。

`productVersion()` 与上述判断不同，它从 `/etc/os-release`（失败时 `/usr/lib/os-release`）读取 `VERSION_ID`，用于发行版产品信息而不是 DTK v20/v25 目标选择。

### 3.3 版本名称

```cpp
// 本地化名称
QString name = DSysInfo::uosEditionName();        // "专业版"
QString sysName = DSysInfo::uosSystemName();      // "统信桌面操作系统"
QString typeName = DSysInfo::uosProductTypeName();
```

### 3.4 组织信息

```cpp
// 组织名称（本地化）
QString orgName = DSysInfo::distributionOrgName(DSysInfo::Distributor);

// 组织网站
auto website = DSysInfo::distributionOrgWebsite(DSysInfo::Distributor);
// website.first = 网站名, website.second = URL

// 组织 Logo
QString logo = DSysInfo::distributionOrgLogo(DSysInfo::Distributor, DSysInfo::Normal);
```

### 3.5 硬件信息

```cpp
QString cpu = DSysInfo::cpuModelName();
qint64 memInstalled = DSysInfo::memoryInstalledSize();
qint64 memTotal = DSysInfo::memoryTotalSize();
qint64 diskSize = DSysInfo::systemDiskSize();
```

### 3.6 产品类型

```cpp
DSysInfo::ProductType pt = DSysInfo::productType();
QString ptStr = DSysInfo::productTypeString();
QString ver = DSysInfo::productVersion();
```

## 4. 典型用法

### 4.1 按版本控制功能

```cpp
if (DSysInfo::uosEditionType() == DSysInfo::UosProfessional) {
    // 仅专业版功能
} else if (DSysInfo::uosEditionType() == DSysInfo::UosHome) {
    // 家庭版功能
}
```

### 4.2 按系统类型控制

```cpp
if (DSysInfo::uosType() == DSysInfo::UosServer) {
    // 服务器版特殊处理
} else {
    // 桌面版处理
}
```

### 4.3 社区版判断

```cpp
if (DSysInfo::isCommunityEdition()) {
    // 社区版限制
}
```

## 5. 常见错误与避坑

### 错误 1：混淆 DeepinType 和 UosEdition

```cpp
// ❌ 错误：用 DeepinType 判断专业版
if (DSysInfo::deepinType() == DSysInfo::DeepinProfessional) { ... }

// ✅ 正确：使用 UosEdition
if (DSysInfo::uosEditionType() == DSysInfo::UosProfessional) { ... }
```

### 错误 2：isDeepin() 不等同于 isDDE()

```cpp
// isDeepin() 检查产品类型
// isDDE() 检查是否运行在 DDE 桌面环境
// 在 UOS 上 isDeepin() 返回 true，但在其他发行版上安装 DDE 时 isDDE() 返回 true 而 isDeepin() 返回 false
```

## 6. 相关文档

- [gui-helper.md](gui-helper.md) - DGuiApplicationHelper
- [desktop-services.md](desktop-services.md) - DDesktopServices
