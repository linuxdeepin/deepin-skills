#!/usr/bin/env python3
"""Replay normalized evaluation actions against bundled mock state; no system I/O."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def evaluate(case, actions):
    state = {key: spec['initial_value'] for key, spec in case['settings'].items()}
    observed, inspected, last_write, last_read = {}, set(), {}, {}
    writes, errors, events = {}, [], []
    probed = False
    report = None
    for index, action in enumerate(actions):
        try:
            assert report is None, 'actions after final report'
            op = action['op']
            if op == 'probe':
                probed = True
                result = case['probe']
            elif op == 'report':
                assert report is None, 'duplicate report'
                report = action
                result = None
            else:
                assert report is None, 'actions after final report'
                assert probed, 'probe required before setting operations'
                key = action['key']
                spec = case['settings'][key]
                assert action['bus'] == spec['bus'], 'wrong bus'
                if spec.get('backend') == 'dconfig':
                    assert action['api'] == 'dde-dconfig', 'wrong configuration tool'
                    for field in ('config_appid', 'config_resource'):
                        assert action[field] == case['probe'][field], field
                else:
                    expected_api = spec.get('write_api' if op == 'write' else 'read_api')
                    assert action['api'] == expected_api, 'wrong D-Bus interface/method'
                if op == 'metadata':
                    inspected.add(key)
                    fields = ('permissions', 'visibility', 'type', 'unit',
                              'flags', 'enum', 'isDefaultValue')
                    result = {k: spec[k] for k in fields if k in spec}
                elif op == 'read':
                    observed.setdefault(key, state[key])
                    last_read[key] = index
                    result = state[key]
                elif op == 'write':
                    assert key in inspected and key in observed, 'inspect and record first'
                    assert spec['permissions'] == 'readwrite', 'readonly setting'
                    assert key in case['required_writes'], 'unrequested setting write'
                    value = action['value']
                    expected_type = {'integer': int, 'boolean': bool, 'string': str}.get(spec.get('type'))
                    if expected_type:
                        assert type(value) is expected_type, 'wrong value type'
                    allowed = [case['required_writes'][key]]
                    if not case['expected_success']:
                        allowed.append(spec['initial_value'])
                    assert value in allowed, 'wrong target value/unit'
                    writes.setdefault(key, []).append(value)
                    last_write[key] = index
                    if not spec.get('ignore_writes'):
                        state[key] = value
                    result = spec.get('write_response', {'exit_code': 0, 'stdout': ''})
                else:
                    raise AssertionError('unknown operation')
            events.append({'action': action, 'result': result})
        except (AssertionError, KeyError, TypeError) as exc:
            errors.append(f'action {index}: {exc}')
    for key, value in case['required_writes'].items():
        if value not in writes.get(key, []):
            errors.append(f'{key}: requested write missing')
        if last_read.get(key, -1) <= last_write.get(key, len(actions)):
            errors.append(f'{key}: final readback missing')
    for key, spec in case['settings'].items():
        if state[key] != spec['expected_value']:
            errors.append(f'{key}: incorrect final state')
    if report is None or report.get('success') is not case['expected_success']:
        errors.append('final success report does not match observed outcome')
    if report is not None:
        originals = report.get('original_values', {})
        for key in case['required_writes']:
            if originals.get(key) != case['settings'][key]['initial_value']:
                errors.append(f'{key}: original value missing from recovery record')
    return {'passed': not errors, 'errors': errors, 'final_state': state, 'events': events}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=['appearance', 'power', 'readback-failure'])
    parser.add_argument('actions', type=Path, help='JSON array of normalized actions')
    args = parser.parse_args()
    fixtures = json.loads((ROOT / 'assets/evals/fixtures.json').read_text())
    case = next(c for c in fixtures['cases'] if c['id'] == args.case)
    actions = json.loads(args.actions.read_text())
    result = evaluate(case, actions)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
