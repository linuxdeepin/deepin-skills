#!/usr/bin/env python3
"""Detached display recovery worker. Only restores its own saved change."""
from __future__ import annotations

import argparse
import os
import time

from tune_state import Store, TuningError


def recover_due(store, change_id, snapshot, now=None, runner=None):
    from tune_engine import rollback_change
    with store.locked():
        change = store.load(change_id)
        guard = change.get('display_guard', {})
        if guard.get('state') != 'armed' or (time.time() if now is None else now) < guard.get('deadline', 0):
            return None
        guard['state'] = 'expired'
        store.change(change)
        result = rollback_change(store, change_id, snapshot, execute=True, runner=runner)
        change = store.load(change_id)
        change['display_guard']['recovery'] = {'ok': result['ok'], 'complete': result['complete'], 'state': result['state']}
        store.change(change)
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--state-dir', required=True)
    parser.add_argument('--change-id', required=True)
    parser.add_argument('--ready-fd', type=int)
    args = parser.parse_args()
    if args.ready_fd is not None:
        os.write(args.ready_fd, b'1')
        os.close(args.ready_fd)
    store = Store(args.state_dir)
    while True:
        try:
            with store.locked():
                change = store.load(args.change_id)
                guard = change.get('display_guard', {})
                if guard.get('state') != 'armed':
                    return
                remaining = guard['deadline'] - time.time()
            if remaining > 0:
                time.sleep(min(remaining, 0.5))
                continue
            from tune_probe import Probe
            result = recover_due(store, args.change_id, Probe().collect())
            if result is not None:
                return
        except (TuningError, OSError, ValueError) as exc:
            # Apply/confirm may hold the lock; remain alive until recovery can run.
            if '另一个系统调优操作' in str(exc):
                time.sleep(0.2)
                continue
            try:
                with store.locked():
                    change = store.load(args.change_id)
                    change['state'] = 'needs_attention'
                    change['display_guard'].update(state='recovery_failed', error=str(exc))
                    store.change(change)
            except (TuningError, OSError):
                pass
            return


if __name__ == '__main__':
    main()
