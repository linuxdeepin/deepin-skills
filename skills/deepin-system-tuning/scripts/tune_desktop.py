"""Typed, capability-probed DDE/ConfigManager adapters. No shell or GUI automation."""
from __future__ import annotations

import json
import math
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from tune_state import TuningError

DISPLAY = ('user', 'org.deepin.dde.Display1', '/org/deepin/dde/Display1', 'org.deepin.dde.Display1')
POWER = ('system', 'org.deepin.dde.Power1', '/org/deepin/dde/Power1', 'org.deepin.dde.Power1')
IDLE = ('user', POWER[1], POWER[2], POWER[3])
WM = ('user', 'com.deepin.wm', '/com/deepin/wm', 'com.deepin.wm')
EFFECTS = ('user', 'org.kde.KWin', '/Effects', 'org.kde.kwin.Effects')
SCALE = ('user', 'org.deepin.dde.Appearance1', '/org/deepin/dde/Appearance1', 'org.deepin.dde.Appearance1')
CONFIG = ('system', 'org.desktopspec.ConfigManager', '/', 'org.desktopspec.ConfigManager')
MANAGER = 'org.desktopspec.ConfigManager.Manager'
DAEMON = 'org.deepin.dde.daemon'
TREE = 'org.deepin.dde.treeland'


def scalar(value):
    if type(value) is bool:
        return 'true' if value else 'false'
    if type(value) in (str, int, float):
        return str(value)
    raise TuningError('D-Bus 参数必须为已校验的标量')


class Bus:
    def __init__(self, runner):
        self.runner = runner
        self.schemas = {}

    def command(self, endpoint, action, *args):
        bus, name, path, interface = endpoint
        return ['busctl', '--' + bus, '--json=short', '--timeout=3',
                '--allow-interactive-authorization=no', action, name, path, interface,
                *map(str, args)]

    def json(self, argv, call=False):
        result = self.runner(argv, timeout=4)
        if not result.get('ok'):
            raise TuningError((result.get('err') or result.get('out') or 'D-Bus 调用失败').strip()[:400])
        if not result.get('out', '').strip():
            return None
        try:
            data = json.loads(result['out'])['data']
        except (ValueError, KeyError, TypeError) as exc:
            raise TuningError('busctl 未返回可解析的 JSON') from exc
        return data[0] if call and isinstance(data, list) and len(data) == 1 else data

    def get(self, endpoint, prop):
        return self.json(self.command(endpoint, 'get-property', prop))

    def all(self, endpoint):
        bus, name, path, interface = endpoint
        value = self.call((bus, name, path, 'org.freedesktop.DBus.Properties'), 'GetAll', 's', interface)
        return {key: item['data'] for key, item in value.items()}

    def call(self, endpoint, method, signature='', *args):
        return self.json(self.command(endpoint, 'call', method, *([signature, *args] if signature else [])), call=True)

    def set(self, endpoint, prop, signature, value):
        return self.json(self.command(endpoint, 'set-property', prop, signature, scalar(value)))

    def schema(self, endpoint):
        if endpoint in self.schemas:
            return self.schemas[endpoint]
        bus, name, path, interface = endpoint
        result = self.runner(['busctl', '--' + bus, '--timeout=3', '--xml-interface',
                              'introspect', name, path, interface], timeout=4)
        if not result.get('ok'):
            raise TuningError('接口不可用：' + interface)
        try:
            root = ET.fromstring(result['out'])
            node = root if root.tag == 'interface' else root.find("interface[@name='%s']" % interface)
            if node is None:
                raise ValueError('missing interface')
            schema = {'properties': {p.get('name'): (p.get('type'), p.get('access')) for p in node.findall('property')},
                      'methods': {m.get('name'): ''.join(a.get('type') for a in m.findall('arg')
                                                       if a.get('direction', 'in') == 'in') for m in node.findall('method')}}
        except (ET.ParseError, ValueError, TypeError) as exc:
            raise TuningError('无法解析接口：' + interface) from exc
        self.schemas[endpoint] = schema
        return schema


# Semantic IDs are the mutation whitelist. UI availability flags and saved output
# records deliberately stay outside it. Ranges are independent of JSON coercion.
PROPERTIES = {
    'power.mode': (POWER, 'Mode', 's', 'SetMode', ('balance', 'performance', 'powersave')),
    'power.saving': (POWER, 'PowerSavingModeEnabled', 'b', None, None),
    'power.auto_battery': (POWER, 'PowerSavingModeAuto', 'b', None, None),
    'power.auto_low_battery': (POWER, 'PowerSavingModeAutoWhenBatteryLow', 'b', None, None),
    'power.low_battery_percent': (POWER, 'PowerSavingModeAutoBatteryPercent', 'u', None, (5, 50)),
    'power.brightness_drop_percent': (POWER, 'PowerSavingModeBrightnessDropPercent', 'u', None, (0, 80)),
    'display.auto_brightness': (DISPLAY, 'AutoBrightnessEnabled', 'b', 'SetAutoBrightnessEnabled', None),
    'display.color_temperature_mode': (DISPLAY, 'ColorTemperatureMode', 'i', 'SetMethodAdjustCCT', (0, 2)),
    'display.color_temperature': (DISPLAY, 'ColorTemperatureManual', 'i', 'SetColorTemperature', (1000, 10000)),
    'effects.compositing': (WM, 'compositingEnabled', 'b', None, None),
}
for source, prefix in (('ac', 'LinePower'), ('battery', 'Battery')):
    for suffix, prop in (('screen_off', 'ScreenBlackDelay'), ('sleep', 'SleepDelay'), ('lock', 'LockDelay'), ('screensaver', 'ScreensaverDelay')):
        PROPERTIES['idle.' + source + '.' + suffix] = (IDLE, prefix + prop, 'i', None, (0, 86400))
    PROPERTIES['idle.' + source + '.lid_action'] = (IDLE, prefix + 'LidClosedAction', 'i', None, (0, 3))
for key, prop in (('idle.lock_on_sleep', 'SleepLock'), ('idle.lock_on_screen_off', 'ScreenBlackLock')):
    PROPERTIES[key] = (IDLE, prop, 'b', None, None)

# app, resource, key, scalar type, range. Metadata permissions/flags are checked
# again at execution; global settings require noninteractive privilege.
DCONFIG = {
    'effects.opacity': ('org.deepin.dde.appearance', 'org.deepin.dde.appearance', 'Opacity', 'd', (0.1, 1.0)),
    'effects.window_radius': (DAEMON, 'org.deepin.XSettings', 'dtk-window-radius', 'i', (0, 40)),
    'display.auto_scale': (DAEMON, 'org.deepin.Display', 'autoChangeScaleEnabled', 'b', None),
    'input.keyboard.repeat_enabled': (DAEMON, 'org.deepin.dde.daemon.keyboard', 'repeatEnabled', 'b', None),
    'input.keyboard.repeat_interval': (DAEMON, 'org.deepin.dde.daemon.keyboard', 'repeatInterval', 'i', (10, 1000)),
    'input.keyboard.repeat_delay': (DAEMON, 'org.deepin.dde.daemon.keyboard', 'delay', 'i', (100, 2000)),
    'sound.effects': (DAEMON, 'org.deepin.dde.daemon.soundeffect', 'enabled', 'b', None),
    'audio.mono': (DAEMON, 'org.deepin.dde.daemon.audio', 'monoEnabled', 'b', None),
    'audio.noise_reduction': (DAEMON, 'org.deepin.dde.daemon.audio', 'reduceNoiseEnabled', 'b', None),
    'input.mouse.natural_scroll': (DAEMON, 'org.deepin.dde.daemon.mouse', 'naturalScroll', 'b', None),
    'input.mouse.acceleration': (DAEMON, 'org.deepin.dde.daemon.mouse', 'motionAcceleration', 'd', (0.1, 3.0)),
    'input.touchpad.natural_scroll': (DAEMON, 'org.deepin.dde.daemon.touchpad', 'naturalScroll', 'b', None),
    'input.touchpad.tap_to_click': (DAEMON, 'org.deepin.dde.daemon.touchpad', 'tapToClick', 'b', None),
    'input.touchpad.disable_while_typing': (DAEMON, 'org.deepin.dde.daemon.touchpad', 'disableWhileTyping', 'b', None),
}
TREELAND = {
    'effects.blur_strength': ('blurStrength', 'i', (0, 128)),
    'effects.glass': ('glassEnabled', 'b', None),
    'effects.opacity': ('windowOpacity', 'i', (10, 100)),
    'effects.window_radius': ('windowRadius', 'i', (0, 40)),
    'input.keyboard.repeat_delay': ('keyboardDelay', 'i', (100, 2000)),
    'input.keyboard.repeat_rate': ('keyboardRate', 'i', (1, 100)),
    'input.mouse.natural_scroll': ('mouseNaturalScroll', 'b', None),
    'input.mouse.acceleration': ('mouseAccelSpeed', 'd', (-1.0, 1.0)),
    'input.touchpad.natural_scroll': ('touchpadNaturalScroll', 'b', None),
    'input.touchpad.tap_to_click': ('touchpadTapToClick', 'b', None),
    'input.touchpad.disable_while_typing': ('touchpadDisableWhileTyping', 'b', None),
}
EFFECT_NAMES = ('blur', 'fade', 'scale', 'minimize', 'slidingpopups')
GUARDED = {'display.mode', 'display.scale', 'display.primary', 'display.layout'}


def validate_value(value, signature, bounds=None):
    valid = ((signature == 'b' and type(value) is bool) or
             (signature in ('i', 'u') and type(value) is int) or
             (signature == 'd' and type(value) in (int, float) and math.isfinite(value)) or
             (signature == 's' and type(value) is str))
    if not valid:
        raise TuningError('设置类型不匹配：期望 ' + signature)
    if bounds:
        if signature == 's':
            valid = value in bounds
        else:
            valid = bounds[0] <= value <= bounds[1]
        if not valid:
            raise TuningError('设置超出允许范围：' + str(bounds))
    return value


class Desktop:
    def __init__(self, runner, root='/', session=None, uid=None):
        self.bus = Bus(runner)
        self.root = Path(root)
        self.session = session or os.environ.get('XDG_SESSION_TYPE', '')
        self.uid = os.getuid() if uid is None else uid
        self.treeland = False
        if self.session == 'wayland':
            for path in self.root.glob('proc/[0-9]*/comm'):
                try:
                    if path.parent.stat().st_uid == self.uid and path.read_text().strip() == 'treeland':
                        self.treeland = True
                        break
                except OSError:
                    continue

    def dconfig_spec(self, setting):
        if self.treeland and setting in TREELAND:
            key, sig, bounds = TREELAND[setting]
            resource = 'org.deepin.dde.treeland.user.seat' if setting.startswith('input.') else 'org.deepin.dde.treeland.user'
            return TREE, resource, key, sig, bounds
        if self.session == 'wayland' and setting in TREELAND:
            return None
        return DCONFIG.get(setting)

    def metadata(self, spec):
        app, resource, key, _, _ = spec
        path = self.root / 'usr/share/dsg/configs' / app / (resource + '.json')
        try:
            data = json.loads(path.read_text(encoding='utf-8'))['contents'][key]
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise TuningError('dconfig 元数据缺失：' + resource + '/' + key) from exc
        if data.get('permissions') != 'readwrite':
            raise TuningError('dconfig 项不可写：' + key)
        return data

    def manager(self, spec):
        app, resource, _, _, _ = spec
        path = self.bus.call(CONFIG, 'acquireManagerV2', 'usss', self.uid, app, resource, '')
        if not isinstance(path, str) or not path.startswith('/'):
            raise TuningError('无效的 ConfigManager 对象路径')
        return ('system', CONFIG[1], path, MANAGER)

    def dconfig_read(self, spec):
        self.metadata(spec)
        endpoint = self.manager(spec)
        try:
            if self.bus.call(endpoint, 'permissions', 's', spec[2]) != 'readwrite':
                raise TuningError('当前策略禁止修改此 dconfig 项')
            variant = self.bus.call(endpoint, 'value', 's', spec[2])
            default = self.bus.call(endpoint, 'isDefaultValue', 's', spec[2])
            if not isinstance(variant, dict) or variant.get('type') not in ('b', 'i', 'u', 'x', 't', 'd', 's'):
                raise TuningError('dconfig 返回了不支持的类型')
            validate_value(variant['data'], spec[3])
            return {'value': variant['data'], 'default': default, 'signature': variant['type']}
        finally:
            self.bus.call(endpoint, 'release')

    def monitor(self, name):
        for path in self.bus.get(DISPLAY, 'Monitors'):
            if not re.fullmatch(r'/org/deepin/dde/Display1/Monitor_[A-Za-z0-9_]+', path):
                continue
            ep = ('user', DISPLAY[1], path, DISPLAY[3] + '.Monitor')
            if self.bus.get(ep, 'Name') == name and self.bus.get(ep, 'Connected'):
                return ep
        raise TuningError('显示器已断开或不存在：' + str(name))

    def read(self, target):
        key = target['setting']
        if key.startswith('input.'):
            spec = self.dconfig_spec(key)
            if self.session == 'wayland' and not self.treeland:
                raise TuningError('未知 Wayland 合成器的输入后端')
        if key in PROPERTIES:
            ep, prop, _, _, _ = PROPERTIES[key]
            return {'value': self.bus.get(ep, prop)}
        if key == 'display.brightness':
            name = target['monitor']
            if not self.bus.get(DISPLAY, 'CanSetBrightnessMap').get(name):
                raise TuningError('此输出不支持亮度设置：' + name)
            return {'value': self.bus.get(DISPLAY, 'Brightness')[name]}
        if key == 'display.mode':
            ep = self.monitor(target['monitor'])
            mode = self.bus.get(ep, 'CurrentMode')
            return {'value': list(mode), 'monitor': target['monitor']}
        if key == 'display.primary':
            return {'value': self.bus.get(DISPLAY, 'Primary')}
        if key == 'display.layout':
            ep = self.monitor(target['monitor'])
            return {'value': [self.bus.get(ep, 'X'), self.bus.get(ep, 'Y')]}
        if key == 'display.scale':
            values = self.bus.call(SCALE, 'GetScreenScaleFactors')
            return {'value': values.get(target['monitor'], self.bus.call(SCALE, 'GetScaleFactor')),
                    'explicit': target['monitor'] in values}
        if key.startswith('effects.') and key.split('.')[-1] in EFFECT_NAMES:
            return {'value': self.bus.call(EFFECTS, 'isEffectLoaded', 's', key.split('.')[-1])}
        spec = self.dconfig_spec(key)
        if spec:
            return self.dconfig_read(spec)
        raise TuningError('不支持的桌面设置：' + key)

    def validate(self, target, value, restoring=False):
        key = target['setting']
        if key == 'effects.compositing' and self.session != 'x11':
            raise TuningError('当前会话不支持切换 X11 合成器')
        if self.session == 'wayland' and key.startswith('input.keyboard.') and key not in TREELAND:
            raise TuningError('当前会话未提供对应键盘设置')
        if key in PROPERTIES:
            ep, prop, sig, method, bounds = PROPERTIES[key]
            validate_value(value, sig, None if restoring else bounds)
            schema = self.bus.schema(ep)
            if schema['properties'].get(prop, (None,))[0] != sig:
                raise TuningError('属性类型不匹配：' + prop)
            if method:
                if schema['methods'].get(method) != sig:
                    raise TuningError('写入方法不可用：' + method)
            elif schema['properties'][prop][1] != 'readwrite':
                raise TuningError('属性不可写：' + prop)
            if key == 'power.mode' and value == 'performance' and not restoring:
                if not self.bus.get(POWER, 'IsHighPerformanceSupported'):
                    raise TuningError('此硬件或电源后端不支持性能模式')
            if key == 'effects.compositing':
                if not self.bus.get(WM, 'compositingPossible') or not self.bus.get(WM, 'compositingAllowSwitch'):
                    raise TuningError('当前窗口管理器禁止切换合成状态')
            if key == 'display.auto_brightness' and value and not self.bus.get(DISPLAY, 'AutoBrightnessSupported'):
                raise TuningError('当前设备不支持自动亮度')
        elif key == 'display.brightness':
            if self.bus.schema(DISPLAY)['methods'].get('SetAndSaveBrightness') != 'sd':
                raise TuningError('缺少可持久化的亮度接口')
            validate_value(value, 'd', (0.0, 1.0) if restoring else (0.05, 1.0))
            self.read(target)
        elif key == 'display.mode':
            ep = self.monitor(target['monitor'])
            if self.bus.schema(ep)['methods'].get('SetMode') != 'u':
                raise TuningError('缺少显示模式写入接口')
            self.validate_commit()
            if type(value) is not list or len(value) != 4 or value not in self.bus.get(ep, 'Modes'):
                raise TuningError('分辨率和刷新率组合不在当前输出支持的模式中')
        elif key == 'display.primary':
            validate_value(value, 's')
            self.monitor(value)
            if self.bus.schema(DISPLAY)['methods'].get('SetPrimary') != 's':
                raise TuningError('缺少主屏设置接口')
            self.validate_commit()
        elif key == 'display.layout':
            ep = self.monitor(target['monitor'])
            if self.bus.schema(ep)['methods'].get('SetPosition') != 'nn':
                raise TuningError('缺少输出布局接口')
            self.validate_commit()
            if not isinstance(value, list) or len(value) != 2:
                raise TuningError('位置必须为 [x,y]')
            for item in value:
                validate_value(item, 'i', (-32768, 32767))
        elif key == 'display.scale':
            self.monitor(target['monitor'])
            validate_value(value, 'd', (1.0, 3.0))
            if self.bus.schema(SCALE)['methods'].get('SetScreenScaleFactors') != 'a{sd}':
                raise TuningError('当前会话不支持按屏缩放')
        elif key.startswith('effects.') and key.split('.')[-1] in EFFECT_NAMES:
            validate_value(value, 'b')
            if not self.bus.call(EFFECTS, 'isEffectSupported', 's', key.split('.')[-1]):
                raise TuningError('当前合成器不支持此特效')
        else:
            spec = self.dconfig_spec(key)
            if not spec:
                raise TuningError('桌面设置不在白名单中：' + key)
            self.metadata(spec)
            validate_value(value, spec[3], None if restoring else spec[4])

    def validate_commit(self):
        methods = self.bus.schema(DISPLAY)['methods']
        if any(methods.get(key) != '' for key in ('ApplyChanges', 'Save', 'ResetChanges')):
            raise TuningError('缺少显示提交、保存或重置接口')

    def write(self, target, value, reset=False, signature=None, restoring=False):
        self.validate(target, value, restoring=restoring)
        key = target['setting']
        if key in PROPERTIES:
            ep, prop, sig, method, _ = PROPERTIES[key]
            if method:
                self.bus.call(ep, method, sig, scalar(value))
            else:
                self.bus.set(ep, prop, sig, value)
        elif key == 'display.brightness':
            self.bus.call(DISPLAY, 'SetAndSaveBrightness', 'sd', target['monitor'], value)
        elif key == 'display.mode':
            ep = self.monitor(target['monitor'])
            try:
                self.bus.call(ep, 'SetMode', 'u', value[0])
                self.bus.call(DISPLAY, 'ApplyChanges')
                self.bus.call(DISPLAY, 'Save')
            except TuningError:
                self.bus.call(DISPLAY, 'ResetChanges')
                raise
        elif key == 'display.primary':
            self.bus.call(DISPLAY, 'SetPrimary', 's', value)
            self.bus.call(DISPLAY, 'ApplyChanges')
            self.bus.call(DISPLAY, 'Save')
        elif key == 'display.layout':
            self.bus.call(self.monitor(target['monitor']), 'SetPosition', 'nn', *value)
            self.bus.call(DISPLAY, 'ApplyChanges')
            self.bus.call(DISPLAY, 'Save')
        elif key == 'display.scale':
            values = self.bus.call(SCALE, 'GetScreenScaleFactors')
            if reset:
                values.pop(target['monitor'], None)
            else:
                values[target['monitor']] = value
            args = [len(values)]
            for name, scale in sorted(values.items()):
                args += [name, scale]
            self.bus.call(SCALE, 'SetScreenScaleFactors', 'a{sd}', *args)
        elif key.startswith('effects.') and key.split('.')[-1] in EFFECT_NAMES:
            result = self.bus.call(EFFECTS, 'loadEffect' if value else 'unloadEffect', 's', key.split('.')[-1])
            if value and result is False:
                raise TuningError('合成器拒绝加载特效')
        else:
            spec = self.dconfig_spec(key)
            ep = self.manager(spec)
            try:
                if self.bus.call(ep, 'permissions', 's', spec[2]) != 'readwrite':
                    raise TuningError('当前策略禁止修改此 dconfig 项')
                if reset:
                    self.bus.call(ep, 'reset', 's', spec[2])
                else:
                    self.bus.call(ep, 'setValue', 'sv', spec[2], signature or spec[3], scalar(value))
            finally:
                self.bus.call(ep, 'release')

    def preview(self, target, value, before=None):
        key = target['setting']
        command = self.bus.command
        if key in PROPERTIES:
            ep, prop, sig, method, _ = PROPERTIES[key]
            return [command(ep, 'call', method, sig, scalar(value)) if method else command(ep, 'set-property', prop, sig, scalar(value))]
        if key == 'display.brightness':
            return [command(DISPLAY, 'call', 'SetAndSaveBrightness', 'sd', target['monitor'], value)]
        if key in ('display.mode', 'display.layout', 'display.primary'):
            if key == 'display.mode':
                first = command(self.monitor(target['monitor']), 'call', 'SetMode', 'u', value[0])
            elif key == 'display.layout':
                first = command(self.monitor(target['monitor']), 'call', 'SetPosition', 'nn', *value)
            else:
                first = command(DISPLAY, 'call', 'SetPrimary', 's', value)
            return [first, command(DISPLAY, 'call', 'ApplyChanges'), command(DISPLAY, 'call', 'Save')]
        if key == 'display.scale':
            values = self.bus.call(SCALE, 'GetScreenScaleFactors')
            if before and before.get('explicit') is False:
                values.pop(target['monitor'], None)
            else:
                values[target['monitor']] = value
            args = [len(values)]
            for name, scale in sorted(values.items()):
                args += [name, scale]
            return [command(SCALE, 'call', 'SetScreenScaleFactors', 'a{sd}', *args)]
        if key.startswith('effects.') and key.split('.')[-1] in EFFECT_NAMES:
            return [command(EFFECTS, 'call', 'loadEffect' if value else 'unloadEffect', 's', key.split('.')[-1])]
        spec = self.dconfig_spec(key)
        if not spec:
            raise TuningError('未知桌面设置')
        ep = self.manager(spec)
        self.bus.call(ep, 'release')
        if before and before.get('default'):
            return [command(ep, 'call', 'reset', 's', spec[2])]
        return [command(ep, 'call', 'setValue', 'sv', spec[2], (before or {}).get('signature', spec[3]), scalar(value))]


def inventory(root='/'):
    """Expose installed resource coverage, including readonly and unhandled keys."""
    resources = []
    for app in (DAEMON, TREE, 'org.deepin.dde.control-center', 'org.kde.kwin', 'org.deepin.dde.appearance'):
        for path in sorted((Path(root) / 'usr/share/dsg/configs' / app).glob('*.json')):
            try:
                contents = json.loads(path.read_text())['contents']
                resources.append({'app_id': app, 'resource': path.stem,
                                  'keys': [{'key': k, 'permissions': v.get('permissions'),
                                            'flags': v.get('flags', [])} for k, v in contents.items()]})
            except (OSError, ValueError, KeyError, TypeError):
                continue
    return resources


def discover(runner, root='/', session=None):
    desktop = Desktop(runner, root, session)
    result = {'session': desktop.session, 'settings': {}, 'monitors': [], 'errors': [],
              'dconfig_resources': inventory(root)}
    # Bulk reads keep collection bounded and avoid one subprocess per property.
    for endpoint in dict.fromkeys(item[0] for item in PROPERTIES.values()):
        if endpoint == WM and desktop.session != 'x11':
            continue
        try:
            schema = desktop.bus.schema(endpoint)
            values = desktop.bus.all(endpoint)
            for key, (ep, prop, sig, method, bounds) in PROPERTIES.items():
                if ep != endpoint or prop not in values:
                    continue
                writable = schema['methods'].get(method) == sig if method else schema['properties'].get(prop) == (sig, 'readwrite')
                if writable:
                    result['settings'][key] = {'value': values[prop], 'backend': 'dbus', 'runtime_verified': True,
                                               'signature': sig, 'range': bounds, 'scope': 'system' if ep[0] == 'system' else 'user'}
            if endpoint == DISPLAY:
                result['auto_brightness_supported'] = values.get('AutoBrightnessSupported', False)
                result['primary'] = values.get('Primary')
                result['display_pending'] = values.get('HasChanged', False)
                for path in values.get('Monitors', []):
                    ep = ('user', DISPLAY[1], path, DISPLAY[3] + '.Monitor')
                    item = desktop.bus.all(ep)
                    if not item.get('Connected') or not item.get('Enabled'):
                        continue
                    name = item['Name']
                    result['monitors'].append({'name': name, 'mode': item['CurrentMode'], 'modes': item['Modes'],
                                               'best_mode': item.get('BestMode'), 'position': [item.get('X'), item.get('Y')],
                                               'brightness': values.get('Brightness', {}).get(name),
                                               'can_brightness': values.get('CanSetBrightnessMap', {}).get(name, False)})
        except (TuningError, KeyError, TypeError) as exc:
            result['errors'].append(str(exc))
    try:
        scales = desktop.bus.call(SCALE, 'GetScreenScaleFactors')
        for monitor in result['monitors']:
            monitor['scale'] = scales.get(monitor['name'], desktop.bus.call(SCALE, 'GetScaleFactor'))
    except (TuningError, TypeError):
        pass
    if desktop.session == 'x11':
        for effect in EFFECT_NAMES:
            try:
                if desktop.bus.call(EFFECTS, 'isEffectSupported', 's', effect):
                    value = desktop.bus.call(EFFECTS, 'isEffectLoaded', 's', effect)
                    result['settings']['effects.' + effect] = {'value': value, 'backend': 'kwin-runtime', 'runtime_verified': True, 'scope': 'session'}
            except TuningError:
                break
    for key in DCONFIG.keys() | TREELAND.keys():
        spec = desktop.dconfig_spec(key)
        if not spec:
            continue
        # Installed Treeland schemas do not mean this is a Treeland session.
        if desktop.session == 'wayland' and not desktop.treeland and key in TREELAND:
            continue
        try:
            meta = desktop.metadata(spec)
            state = desktop.dconfig_read(spec)
            result['settings'][key] = {**state, 'backend': 'dconfig', 'runtime_verified': False,
                                       'scope': 'system' if 'global' in meta.get('flags', []) else 'user',
                                       'app_id': spec[0], 'resource': spec[1], 'key': spec[2], 'range': spec[4]}
        except TuningError:
            continue
    supported = {(item.get('app_id'), item.get('resource'), item.get('key')): key
                 for key, item in result['settings'].items() if item.get('backend') == 'dconfig'}
    for resource in result['dconfig_resources']:
        for item in resource['keys']:
            item['setting'] = supported.get((resource['app_id'], resource['resource'], item['key']))
            item['coverage'] = 'supported' if item['setting'] else ('readonly' if item['permissions'] != 'readwrite' else 'inventory_only')
    return result
