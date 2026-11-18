"""Orthogonal desktop components, explicit overrides and semantic constraints."""
from __future__ import annotations

import copy

from tune_desktop import DCONFIG, EFFECT_NAMES, GUARDED, PROPERTIES, TREELAND, validate_value
from tune_state import TuningError

COMPONENTS = {
    'display-native': '原生显示模式',
    'display-high-refresh': '当前分辨率最高刷新率',
    'display-battery': '当前分辨率最低刷新率与适度亮度',
    'effects-quality': '保留合成与窗口特效',
    'effects-reduced': '减少模糊与窗口动画',
    'idle-balanced': '按交流电和电池分别设置熄屏、锁屏与休眠',
    'idle-battery': '缩短电池空闲时间',
    'color-accurate': '关闭自动色温',
}
SCENARIOS = {
    'comfort-office': ('办公舒适', ['power-balanced', 'graphics-quality', 'display-native', 'effects-quality', 'idle-balanced']),
    'coding-smooth': ('编程流畅', ['dev-limits', 'graphics-performance', 'display-high-refresh', 'effects-reduced']),
    'long-battery': ('长续航', ['power-battery', 'display-battery', 'effects-reduced', 'idle-battery']),
    'gaming-low-latency': ('游戏低延迟', ['power-performance', 'graphics-performance', 'display-high-refresh', 'effects-reduced']),
    'design-accurate': ('设计与色彩准确', ['power-balanced', 'graphics-quality', 'display-native', 'effects-quality', 'color-accurate']),
}


def op(profile, setting, value, snapshot, monitor=None):
    native = snapshot.get('desktop_native') or {}
    capability = native.get('settings', {}).get(setting, {})
    config_setting = setting in (set(DCONFIG) | set(TREELAND)) and setting not in PROPERTIES and setting not in {'effects.' + e for e in EFFECT_NAMES}
    backend = capability.get('backend', 'dconfig' if config_setting else 'dbus')
    target = {'setting': setting, 'session': native.get('session', ''),
              'backend': backend}
    if monitor:
        target['monitor'] = monitor
    return {'profile': profile, 'category': setting.split('.')[0], 'kind': 'desktop',
            'title': setting + (':' + monitor if monitor else ''),
            'description': '通过已探测的 DDE/ConfigManager 接口设置并保存原值。',
            'target': target, 'desired': {'value': value}, 'requires_root': capability.get('backend') == 'dconfig' and capability.get('scope') == 'system',
            'runtime_verifiable': capability.get('runtime_verified', backend != 'dconfig'),
            'relogin_required': setting == 'display.scale', 'restart_required': False,
            'reboot_required': False, 'display_guard': setting in GUARDED,
            'executable': not ('desktop_native' in snapshot and not monitor and setting != 'display.primary' and setting not in native.get('settings', {})),
            'reason': '当前会话未探测到此设置能力' if 'desktop_native' in snapshot and not monitor and setting != 'display.primary' and setting not in native.get('settings', {}) else None}


def settings_ops(snapshot, settings, profile='explicit'):
    """Resolve outputs into one mode per monitor; refresh is never independent."""
    if not isinstance(settings, dict):
        raise TuningError('settings 必须为对象')
    settings = copy.deepcopy(settings)
    outputs = settings.pop('outputs', {})
    if not isinstance(outputs, dict):
        raise TuningError('outputs 必须为显示器名称到设置对象的映射')
    native = snapshot.get('desktop_native') or {}
    monitors = {m['name']: m for m in native.get('monitors', [])}
    result = []
    for name, values in outputs.items():
        if name not in monitors or not isinstance(values, dict):
            raise TuningError('未知显示器或无效设置：' + str(name))
        if set(values) - {'resolution', 'refresh', 'brightness', 'scale', 'position'}:
            raise TuningError('输出设置只支持 resolution、refresh、brightness、scale、position')
        monitor = monitors[name]
        if 'resolution' in values or 'refresh' in values:
            resolution = values.get('resolution', monitor['mode'][1:3])
            if not isinstance(resolution, list) or len(resolution) != 2 or any(type(x) is not int or not 320 <= x <= 32768 for x in resolution):
                raise TuningError('resolution 必须为 [宽,高] 的有效整数数组')
            refresh = values.get('refresh')
            if refresh is not None:
                validate_value(refresh, 'd', (1, 1000))
            modes = [mode for mode in monitor['modes'] if mode[1:3] == resolution and
                     (refresh is None or abs(mode[3] - refresh) < 0.1)]
            if not modes:
                raise TuningError('不支持的分辨率与刷新率组合：' + name)
            mode = min(modes, key=lambda m: abs(m[3] - (refresh or monitor['mode'][3])))
            result.append(op(profile, 'display.mode', mode, snapshot, name))
        for field, setting in (('brightness', 'display.brightness'), ('scale', 'display.scale'), ('position', 'display.layout')):
            if field in values:
                result.append(op(profile, setting, values[field], snapshot, name))
    allowed = set(PROPERTIES) | set(DCONFIG) | set(TREELAND) | {'effects.' + k for k in EFFECT_NAMES} | {'display.primary'}
    for key, value in settings.items():
        if key not in allowed:
            raise TuningError('未知设置：' + str(key))
        result.append(op(profile, key, value, snapshot))
    # Automatic policies must be disabled before fixed brightness / colour writes.
    result.sort(key=lambda item: (item['target']['setting'] in GUARDED,
                                  item['target']['setting'] not in ('display.auto_brightness', 'power.saving', 'display.color_temperature_mode')))
    return result


def component_ops(component, snapshot):
    native = snapshot.get('desktop_native') or {}
    available = native.get('settings', {})
    values = {}
    output = {}
    primary = next((m for m in native.get('monitors', []) if m['name'] == native.get('primary')), None)
    if component.startswith('display-') and primary:
        mode = primary['mode']
        candidates = [m for m in primary['modes'] if m[1:3] == mode[1:3]]
        if component == 'display-native':
            best = primary.get('best_mode')
            if best:
                output = {'resolution': best[1:3], 'refresh': best[3]}
        elif candidates:
            chosen = (min if component == 'display-battery' else max)(candidates, key=lambda m: m[3])
            output = {'resolution': chosen[1:3], 'refresh': chosen[3]}
        if component == 'display-battery' and primary.get('can_brightness') and primary.get('brightness') is not None:
            output['brightness'] = max(0.2, min(primary['brightness'], 0.55))
            if 'display.auto_brightness' in available:
                values['display.auto_brightness'] = False
        if output:
            values['outputs'] = {primary['name']: output}
    elif component in ('effects-quality', 'effects-reduced'):
        enabled = component == 'effects-quality'
        for key in available:
            if key in {'effects.' + e for e in EFFECT_NAMES} or key == 'effects.glass':
                values[key] = enabled
        if 'effects.compositing' in available:
            values['effects.compositing'] = True
        if 'effects.blur_strength' in available:
            values['effects.blur_strength'] = 60 if enabled else 0
    elif component in ('idle-balanced', 'idle-battery'):
        for source, times in (('ac', (900, 1800, 900)), ('battery', (180, 900, 180))):
            if component == 'idle-battery' and source == 'ac':
                continue
            for suffix, delay in zip(('screen_off', 'sleep', 'lock'), times):
                key = 'idle.' + source + '.' + suffix
                if key in available:
                    values[key] = delay
    elif component == 'color-accurate' and 'display.color_temperature_mode' in available:
        values['display.color_temperature_mode'] = 0
    operations = settings_ops(snapshot, values, component)
    if not operations:
        operations.append({'profile': component, 'category': 'desktop', 'kind': 'advisory',
                           'title': component, 'description': '当前会话未暴露此组件所需接口，未生成写入项。',
                           'executable': False, 'reason': '接口或硬件能力不可用'})
    return operations


def constraints(operations, snapshot):
    """Cross-setting constraints, including currently active automatic policies."""
    current = {key: item['value'] for key, item in (snapshot.get('desktop_native') or {}).get('settings', {}).items()}
    desired = dict(current)
    explicit = {}
    conflicts = []
    warnings = []
    for item in operations:
        if item['kind'] == 'desktop':
            key = item['target']['setting']
            desired[key] = item['desired']['value']
            explicit[key] = item
    def conflict(message):
        conflicts.append({'key': ['desktop-policy'], 'profiles': [], 'reason': message})
    if 'power.mode' in explicit and 'power.saving' in explicit and desired.get('power.saving') is True and desired.get('power.mode') != 'powersave':
        conflict('省电开关与固定电源模式冲突；启用省电时选择 power.mode=powersave')
    if 'display.brightness' in explicit and desired.get('display.auto_brightness') is True:
        conflict('固定亮度与自动亮度冲突；显式设置 display.auto_brightness=false')
    if 'display.brightness' in explicit and desired.get('power.saving') is True and desired.get('power.brightness_drop_percent', 0) > 0:
        conflict('省电亮度衰减会覆盖固定亮度；显式设置 power.brightness_drop_percent=0')
    if 'display.color_temperature' in explicit and desired.get('display.color_temperature_mode') != 2:
        conflict('手动色温需要 display.color_temperature_mode=2')
    if desired.get('effects.compositing') is False:
        if any(key in explicit and bool(value) for key, value in desired.items() if key.startswith('effects.') and key != 'effects.compositing'):
            conflict('关闭合成与启用窗口特效冲突')
        warnings.append('关闭合成可能影响透明度、屏幕录制及桌面交互；此设置只适用于支持切换的 X11 会话。')
    if 'power.mode' in explicit and desired.get('power.mode') != 'powersave' and (desired.get('power.auto_battery') or desired.get('power.auto_low_battery')):
        warnings.append('自动电池省电策略可能在电源或电量变化时覆盖所选模式；当前计划不会安装常驻切换守护进程。')
    if any(item.get('display_guard') for item in operations):
        warnings.append('显示模式、布局或缩放变化需在 30 秒内 confirm-display；超时或执行进程退出后由独立守护进程尝试回滚整次变更。')
    if any(item.get('target', {}).get('backend') == 'kwin-runtime' for item in operations):
        warnings.append('KWin 特效通过运行接口切换，仅保证当前合成器会话；重新登录后可能恢复原配置。')
    return conflicts, warnings
