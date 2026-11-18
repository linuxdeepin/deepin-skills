"""Read-only hardware, desktop and service discovery for deepin-system-tuning.

The probe never writes to the system.  Commands are a fixed allowlist and are
always executed as argv arrays, never through a shell.  A temporary root can be
supplied by tests to parse fixture files without touching the host.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

MAX_FILE = 1024 * 1024
INTERESTING_UNITS = (
    "fstrim.timer",
    "systemd-oomd.service",
    "irqbalance.service",
    "thermald.service",
    "power-profiles-daemon.service",
    "tuned.service",
    "tlp.service",
    "earlyoom.service",
    "NetworkManager.service",
    "postgresql.service",
    "mariadb.service",
    "mysql.service",
    "redis-server.service",
)
GSETTINGS_SCHEMAS = (
    "com.deepin.dde.power",
    "com.deepin.wrap.gnome.desktop.interface",
    "org.gnome.desktop.interface",
    "com.deepin.dde.appearance",
    "com.deepin.dde.display",
)


def run(argv, timeout=4.0, env=None):
    """Run one allowlisted command and return a small, JSON-safe result."""
    command = [str(item) for item in argv]
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "LC_ALL": "C", "LANG": "C", **(env or {})},
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "code": None, "out": "", "err": str(exc)}
    return {
        "ok": completed.returncode == 0,
        "code": completed.returncode,
        "out": (completed.stdout or "").strip(),
        "err": (completed.stderr or "").strip(),
    }


def command_exists(name):
    return shutil.which(name) is not None


def read_text(path, default=""):
    try:
        if Path(path).stat().st_size > MAX_FILE:
            return default
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return default


def read_int(path, default=None):
    value = read_text(path).strip()
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def read_key_values(path):
    values = {}
    for line in read_text(path).splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
    return values


def parse_os_release(path):
    values = {}
    for line in read_text(path).splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"')
    return values


class Probe:
    def __init__(self, root="/", home=None, runner=None, env=None):
        self.root = Path(root).resolve()
        self.home = Path(home or os.environ.get("HOME") or Path.home()).expanduser()
        self.runner = runner or run
        self.env = dict(os.environ if env is None else env)
        self._command_cache = {}
        self._services_cache = None

    # ------------------------------------------------------------------ paths
    def p(self, relative):
        return self.root / relative.lstrip("/")

    def exists(self, relative):
        return self.p(relative).exists()

    def cmd(self, argv, timeout=4.0, env=None):
        key = tuple(str(x) for x in argv)
        if timeout == 4.0 and env is None and key in self._command_cache:
            return self._command_cache[key]
        result = self.runner([str(x) for x in argv], timeout=timeout, env=env)
        if timeout == 4.0 and env is None:
            self._command_cache[key] = result
        return result

    def which(self, name):
        return shutil.which(name) is not None

    # --------------------------------------------------------------- overview
    def collect(self):
        machines = {
            "home": str(self.home),
            "host": self.host(),
            "cpu": self.cpu(),
            "memory": self.memory(),
            "gpu": self.gpu(),
            "storage": self.storage(),
            "power": self.power(),
            "desktop": self.desktop(),
            "services": self.services(),
            "network": self.network(),
            "kernel": self.kernel(),
            "databases": self.databases(),
            "tools": self.tools(),
            "capabilities": self.capabilities(),
            "metrics": self.metrics(),
        }
        from tune_desktop import discover
        machines["desktop_native"] = discover(self.runner, str(self.root), self.env.get("XDG_SESSION_TYPE")) if self.which("busctl") else {"settings": {}, "monitors": [], "errors": ["缺少 busctl"]}
        machines["hardware_hash"] = hardware_hash(machines)
        machines["classification"] = classify(machines)
        machines["collected_at"] = int(time.time())
        return machines

    # ---------------------------------------------------------------- sections
    def host(self):
        release = parse_os_release(self.p("etc/os-release"))
        product = read_text(self.p("sys/class/dmi/id/product_name")).strip()
        board = read_text(self.p("sys/class/dmi/id/board_name")).strip()
        chassis = read_text(self.p("sys/class/dmi/id/chassis_type")).strip()
        container = read_text(self.p("run/systemd/container")).strip()
        virt = ""
        if container:
            virt = "container:" + container
        elif self.exists("proc/1/environ"):
            # Do not expose the full environment; only detect common guests.
            environ = read_text(self.p("proc/1/environ"), "")
            for marker in ("KVM", "VMware", "VirtualBox", "Hyper-V", "Xen"):
                if marker.lower() in environ.lower():
                    virt = marker
                    break
        return {
            "hostname": os.uname().nodename,
            "os": {
                "id": release.get("ID"),
                "name": release.get("PRETTY_NAME"),
                "version": release.get("VERSION_ID"),
            },
            "kernel": os.uname().release,
            "arch": os.uname().machine,
            "product": product,
            "board": board,
            "chassis_type": chassis,
            "virtualization": virt or None,
            "boot_id": read_text(self.p("proc/sys/kernel/random/boot_id")).strip() or None,
        }

    def cpu(self):
        info = {}
        for line in read_text(self.p("proc/cpuinfo")).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                info.setdefault(key.strip(), value.strip())
        cpus = sorted(glob.glob(str(self.p("sys/devices/system/cpu/cpu[0-9]*"))))
        cores = {}
        capacities = {}
        core_types = {}
        frequencies = {}
        governors = set()
        epps = set()
        max_freqs = []
        for cpu_path in cpus:
            cpu = Path(cpu_path)
            package = read_text(cpu / "topology/physical_package_id", "0").strip() or "0"
            core_id = read_text(cpu / "topology/core_id", "").strip()
            if core_id == "":
                core_id = cpu.name
            key = package + ":" + core_id
            capacity = read_int(cpu / "cpu_capacity")
            if capacity is not None:
                capacities[key] = capacity
            core_type = read_text(cpu / "topology/core_type", "").strip()
            if core_type:
                core_types[key] = core_type
            max_freq = read_int(cpu / "cpufreq/cpuinfo_max_freq")
            if max_freq:
                frequencies[key] = max(frequencies.get(key, 0), max_freq)
            cores[key] = True
            governor = read_text(cpu / "cpufreq/scaling_governor").strip()
            if governor:
                governors.add(governor)
            epp = read_text(cpu / "cpufreq/energy_performance_preference").strip()
            if epp:
                epps.add(epp)
            freq = read_int(cpu / "cpufreq/cpuinfo_max_freq")
            if freq:
                max_freqs.append(freq // 1000)
        first = Path(cpus[0]) if cpus else None
        scaling_driver = read_text(first / "cpufreq/scaling_driver").strip() if first else ""
        p_cores = e_cores = None
        hybrid = False
        effective = capacities or {}
        if frequencies and (not effective or len(set(effective.values())) == 1):
            effective = frequencies
        if effective:
            high = max(effective.values())
            low = min(effective.values())
            hybrid = low > 0 and high >= low * 1.2
            p_cores = sum(1 for value in effective.values() if value == high)
            e_cores = sum(1 for value in effective.values() if value != high)
        if core_types and len(set(core_types.values())) > 1:
            hybrid = True
        return {
            "model": info.get("model name"),
            "vendor": info.get("vendor_id"),
            "family": info.get("cpu family"),
            "logical": len(cpus) or os.cpu_count(),
            "physical": len(cores) or None,
            "hybrid": hybrid,
            "p_cores": p_cores,
            "e_cores": e_cores,
            "scaling_driver": scaling_driver or None,
            "governor": sorted(governors)[0] if governors else None,
            "governors": sorted(governors),
            "energy_performance_preference": sorted(epps)[0] if epps else None,
            "max_mhz": max(max_freqs) if max_freqs else None,
            "intel_pstate": {
                "status": read_text(self.p("sys/devices/system/cpu/intel_pstate/status")).strip() or None,
                "no_turbo": read_int(self.p("sys/devices/system/cpu/intel_pstate/no_turbo")),
                "hwp_dynamic_boost": read_int(self.p("sys/devices/system/cpu/intel_pstate/hwp_dynamic_boost")),
            },
            "amd_pstate": read_text(self.p("sys/devices/system/cpu/amd_pstate/status")).strip() or None,
        }

    def memory(self):
        info = {}
        for line in read_text(self.p("proc/meminfo")).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                parts = value.split()
                if parts:
                    try:
                        info[key.strip()] = int(parts[0])
                    except ValueError:
                        pass
        zram = []
        for path in sorted(glob.glob(str(self.p("sys/block/zram*")))):
            block = Path(path)
            zram.append({
                "name": block.name,
                "disksize_mb": (read_int(block / "disksize", 0) or 0) // (1024 * 1024),
                "algorithm": read_text(block / "comp_algorithm").strip() or None,
            })
        return {
            "total_mb": (info.get("MemTotal") or 0) // 1024,
            "available_mb": (info.get("MemAvailable") or 0) // 1024,
            "swap_total_mb": (info.get("SwapTotal") or 0) // 1024,
            "swap_free_mb": (info.get("SwapFree") or 0) // 1024,
            "zram": zram,
            "swappiness": read_int(self.p("proc/sys/vm/swappiness")),
            "vfs_cache_pressure": read_int(self.p("proc/sys/vm/vfs_cache_pressure")),
            "dirty_ratio": read_int(self.p("proc/sys/vm/dirty_ratio")),
            "dirty_background_ratio": read_int(self.p("proc/sys/vm/dirty_background_ratio")),
            "laptop_mode": read_int(self.p("proc/sys/vm/laptop_mode")),
            "overcommit_memory": read_int(self.p("proc/sys/vm/overcommit_memory")),
            "transparent_hugepage": read_text(self.p("sys/kernel/mm/transparent_hugepage/enabled")).strip() or None,
        }

    def gpu(self):
        cards = []
        for path in sorted(glob.glob(str(self.p("sys/class/drm/card[0-9]*")))):
            block = Path(path)
            if not re.fullmatch(r"card\d+", block.name) or not (block / "device").exists():
                continue
            device = block / "device"
            try:
                driver = (device / "driver").resolve().name
            except OSError:
                driver = read_text(device / "uevent").split("DRIVER=")[-1].splitlines()[0] if "DRIVER=" in read_text(device / "uevent") else ""
            vendor = read_text(device / "vendor").strip()
            device_id = read_text(device / "device").strip()
            cards.append({
                "card": block.name,
                "pci_id": "%s:%s" % (vendor.replace("0x", ""), device_id.replace("0x", "")),
                "driver": driver or None,
                "driver_module": read_text(device / "driver/module").strip() or None,
                "boot_vga": read_text(device / "boot_vga").strip() == "1",
                "class": read_text(device / "class").strip() or None,
            })
        names = []
        if self.which("lspci"):
            result = self.cmd(["lspci", "-Dnn"], timeout=3)
            if result["ok"]:
                for line in result["out"].splitlines():
                    if re.search(r"\b(VGA compatible controller|3D controller|Display controller)\b", line):
                        names.append(line.strip())
        glx = self.glx()
        nvidia = self.nvidia()
        vaapi = self.vaapi()
        vulkan = self.vulkan()
        vaapi_drivers = []
        for pattern in ("usr/lib/x86_64-linux-gnu/dri/*_drv_video.so", "usr/lib64/dri/*_drv_video.so"):
            vaapi_drivers.extend(sorted(os.path.basename(path) for path in glob.glob(str(self.p(pattern)))))
        return {
            "cards": cards,
            "names": names,
            "gl": glx,
            "nvidia": nvidia,
            "vaapi": vaapi,
            "vaapi_drivers": sorted(set(vaapi_drivers)),
            "vulkan": vulkan,
            "display": self.display(),
            "env": {
                "DRI_PRIME": self.env.get("DRI_PRIME"),
                "__NV_PRIME_RENDER_OFFLOAD": self.env.get("__NV_PRIME_RENDER_OFFLOAD"),
                "__GLX_VENDOR_LIBRARY_NAME": self.env.get("__GLX_VENDOR_LIBRARY_NAME"),
                "LIBVA_DRIVER_NAME": self.env.get("LIBVA_DRIVER_NAME"),
                "mesa_glthread": self.env.get("mesa_glthread"),
            },
        }

    def glx(self):
        if not (self.env.get("DISPLAY") or self.env.get("WAYLAND_DISPLAY")):
            return None
        if not self.which("glxinfo"):
            return None
        result = self.cmd(["glxinfo", "-B"], timeout=5)
        if not result["ok"]:
            return None
        values = {}
        for line in result["out"].splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                values[key.strip()] = value.strip()
        version = None
        match = re.search(r"Mesa\s+([0-9][0-9.]+)", values.get("OpenGL version string", "") + " " + values.get("OpenGL core profile version string", ""))
        if match:
            version = match.group(1)
        return {
            "renderer": values.get("OpenGL renderer string"),
            "vendor": values.get("OpenGL vendor string"),
            "version": values.get("OpenGL core profile version string") or values.get("OpenGL version string"),
            "mesa": version,
            "accelerated": values.get("Accelerated"),
            "video_memory_mb": values.get("Video memory"),
        }

    def nvidia(self):
        if not self.which("nvidia-smi"):
            return None
        result = self.cmd(["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader,nounits"], timeout=4)
        if not result["ok"]:
            return None
        rows = []
        for line in result["out"].splitlines():
            parts = [item.strip() for item in line.split(",")]
            if len(parts) >= 3:
                rows.append({"name": parts[0], "driver": parts[1], "memory_mb": parts[2]})
        return rows or None

    def vaapi(self):
        if not self.which("vainfo"):
            return None
        result = self.cmd(["vainfo"], timeout=5)
        if not result["ok"]:
            return None
        driver = None
        match = re.search(r"Driver version:\s*(.+)", result["out"])
        if match:
            driver = match.group(1).strip()
        profiles = len(re.findall(r"VAProfile", result["out"]))
        return {"driver": driver, "profiles": profiles}

    def vulkan(self):
        if not self.which("vulkaninfo"):
            return None
        result = self.cmd(["vulkaninfo", "--summary"], timeout=6)
        if not result["ok"]:
            return None
        device = re.search(r"deviceName\s*=\s*(.+)", result["out"])
        driver = re.search(r"driverName\s*=\s*(.+)", result["out"])
        api = re.search(r"apiVersion\s*=\s*(.+)", result["out"])
        return {
            "device": device.group(1).strip() if device else None,
            "driver": driver.group(1).strip() if driver else None,
            "api": api.group(1).strip() if api else None,
        }

    def display(self):
        if not self.which("xrandr") or not self.env.get("DISPLAY"):
            return None
        result = self.cmd(["xrandr", "--query"], timeout=3)
        if not result["ok"]:
            return None
        outputs = []
        current = None
        for line in result["out"].splitlines():
            match = re.match(r"^(\S+)\s+(connected|disconnected)\s*(primary)?", line)
            if match:
                current = {
                    "name": match.group(1),
                    "connected": match.group(2) == "connected",
                    "primary": bool(match.group(3)),
                    "width": None,
                    "height": None,
                    "refresh": None,
                }
                outputs.append(current)
                mode = re.search(r"\b(\d{3,5})x(\d{3,5})\+", line)
                if mode:
                    current["width"] = int(mode.group(1))
                    current["height"] = int(mode.group(2))
                continue
            if current and current["connected"]:
                mode = re.search(r"^\s+(\d{3,5})x(\d{3,5})\s+.*?([0-9.]+)\*", line)
                if mode:
                    if current["width"] is None:
                        current["width"] = int(mode.group(1))
                        current["height"] = int(mode.group(2))
                    if current["refresh"] is None:
                        current["refresh"] = float(mode.group(3))
        return outputs

    def storage(self):
        root_mount = {}
        for line in read_text(self.p("proc/mounts")).splitlines():
            parts = line.split()
            if len(parts) >= 4 and parts[1] == "/":
                root_mount = {"source": parts[0], "fstype": parts[2], "options": parts[3]}
                break
        devices = []
        if self.which("lsblk"):
            result = self.cmd(["lsblk", "-J", "-o", "NAME,TYPE,SIZE,ROTA,MODEL,TRAN,MOUNTPOINTS"], timeout=4)
            if result["ok"]:
                try:
                    payload = json.loads(result["out"])
                    for item in payload.get("blockdevices", []):
                        devices.append({
                            "name": item.get("name"),
                            "type": item.get("type"),
                            "size": item.get("size"),
                            "rotational": item.get("rota"),
                            "model": item.get("model"),
                            "transport": item.get("tran"),
                            "mountpoints": item.get("mountpoints"),
                        })
                except ValueError:
                    pass
        base = None
        source = str(root_mount.get("source", ""))
        if source.startswith("/dev/"):
            name = os.path.basename(source)
            candidates = sorted(glob.glob(str(self.p("sys/block/*"))), key=len, reverse=True)
            for candidate in candidates:
                if name.startswith(os.path.basename(candidate)):
                    base = Path(candidate).name
                    break
        scheduler = None
        rotational = None
        if base:
            raw = read_text(self.p("sys/block/%s/queue/scheduler" % base)).strip()
            match = re.search(r"\[([^\]]+)\]", raw)
            scheduler = match.group(1) if match else (raw or None)
            rotational = read_int(self.p("sys/block/%s/queue/rotational" % base))
        return {
            "root": root_mount,
            "devices": devices,
            "root_disk": base,
            "scheduler": scheduler,
            "rotational": rotational,
            "fstrim": None,
        }

    def power(self):
        batteries = []
        ac_online = None
        for path in sorted(glob.glob(str(self.p("sys/class/power_supply/*")))):
            supply = Path(path)
            kind = read_text(supply / "type").strip()
            if kind == "Battery":
                batteries.append({
                    "name": supply.name,
                    "status": read_text(supply / "status").strip() or None,
                    "capacity": read_int(supply / "capacity"),
                    "energy_full_mwh": read_int(supply / "energy_full"),
                    "energy_full_design_mwh": read_int(supply / "energy_full_design"),
                    "power_now_uw": read_int(supply / "power_now"),
                    "cycle_count": read_int(supply / "cycle_count"),
                    "charge_control_start": read_int(supply / "charge_control_start_threshold"),
                    "charge_control_end": read_int(supply / "charge_control_end_threshold"),
                })
            elif kind == "Mains":
                online = read_text(supply / "online").strip()
                if online in ("0", "1"):
                    ac_online = online == "1"
        profile = read_text(self.p("sys/firmware/acpi/platform_profile")).strip() or None
        profile_choices = read_text(self.p("sys/firmware/acpi/platform_profile_choices")).strip().split() or []
        dde = {}
        if self.which("gsettings") and self._schema_exists("com.deepin.dde.power"):
            for key in ("mode", "power-saving-mode-enabled", "high-performance-enabled"):
                dde[key] = self.gsettings_get("com.deepin.dde.power", key)
        power_profiles = None
        if self.which("powerprofilesctl"):
            result = self.cmd(["powerprofilesctl", "get"], timeout=3)
            if result["ok"]:
                power_profiles = result["out"]
        tuned = None
        if self.which("tuned-adm"):
            result = self.cmd(["tuned-adm", "active"], timeout=3)
            if result["ok"]:
                tuned = result["out"]
        temperatures = []
        for path in sorted(glob.glob(str(self.p("sys/class/thermal/thermal_zone*")))):
            zone = Path(path)
            value = (read_int(zone / "temp", 0) or 0) / 1000.0
            if 0 < value < 150:
                temperatures.append({"type": read_text(zone / "type").strip(), "temp_c": value})
        return {
            "battery_present": bool(batteries),
            "batteries": batteries,
            "ac_online": ac_online,
            "platform_profile": profile,
            "platform_profile_choices": profile_choices,
            "dde": dde,
            "power_profiles": power_profiles,
            "tuned": tuned,
            "temperatures": temperatures[:8],
        }

    def desktop(self):
        sessions = []
        for directory in ("usr/share/xsessions", "usr/share/wayland-sessions"):
            for path in sorted(glob.glob(str(self.p(directory) / "*.desktop"))):
                sessions.append({
                    "file": os.path.basename(path),
                    "type": "wayland" if "wayland" in directory else "x11",
                })
        current = self.env.get("XDG_SESSION_TYPE") or None
        animations = None
        interface_schema = None
        if self.which("gsettings"):
            for schema in ("com.deepin.wrap.gnome.desktop.interface", "org.gnome.desktop.interface"):
                if self._schema_exists(schema):
                    interface_schema = schema
                    animations = self.gsettings_get(schema, "enable-animations")
                    break
        power_schema = self._schema_exists("com.deepin.dde.power")
        return {
            "current_desktop": self.env.get("XDG_CURRENT_DESKTOP"),
            "current_session": current,
            "sessions": sessions,
            "animations": animations,
            "interface_schema": interface_schema,
            "interface_keys": self.gsettings_keys(interface_schema) if interface_schema else [],
            "power_schema": power_schema,
            "power_keys": self.gsettings_keys("com.deepin.dde.power") if power_schema else [],
            "dde": power_schema,
            "dde_dconfig": self.which("dde-dconfig"),
        }

    def services(self):
        if self._services_cache is not None:
            return self._services_cache
        unit_files = {}
        unit_active = {}
        if self.exists("run/systemd/system") and self.which("systemctl"):
            result = self.cmd(["systemctl", "list-unit-files", "--no-legend", "--no-pager"], timeout=4)
            if result["ok"]:
                for line in result["out"].splitlines():
                    parts = line.split()
                    if len(parts) >= 2:
                        unit_files[parts[0]] = parts[1]
            result = self.cmd(["systemctl", "list-units", "--all", "--plain",
                               "--no-legend", "--no-pager"], timeout=4)
            if result["ok"]:
                for line in result["out"].splitlines():
                    parts = line.split()
                    unit = next((part for part in parts if part.endswith(
                        (".service", ".timer", ".socket", ".target", ".mount", ".slice"))), None)
                    if unit is None:
                        continue
                    index = parts.index(unit)
                    if len(parts) > index + 2:
                        unit_active[unit] = parts[index + 2]
        units = {}
        for unit in INTERESTING_UNITS:
            exists = unit in unit_files or unit in unit_active
            units[unit] = {
                "exists": exists,
                "enabled": unit_files.get(unit),
                "active": unit_active.get(unit),
            }
        for unit in sorted(set(unit_files) | set(unit_active)):
            if unit.startswith("postgresql@") and unit.endswith(".service"):
                units[unit] = {
                    "exists": True,
                    "enabled": unit_files.get(unit),
                    "active": unit_active.get(unit),
                }
        self._services_cache = units
        return units

    def network(self):
        interfaces = []
        for path in sorted(glob.glob(str(self.p("sys/class/net/*")))):
            net = Path(path)
            if net.name == "lo":
                continue
            try:
                driver = (net / "device/driver").resolve().name
            except OSError:
                driver = None
            interfaces.append({
                "name": net.name,
                "wireless": (net / "wireless").exists() or (net / "phy80211").exists(),
                "driver": driver,
                "state": read_text(net / "operstate").strip() or None,
                "speed_mbps": read_int(net / "speed"),
            })
        return {
            "interfaces": interfaces,
            "wifi": any(item["wireless"] for item in interfaces),
            "manager": "NetworkManager" if self.services().get("NetworkManager.service", {}).get("exists") else None,
        }

    def kernel(self):
        modules = {}
        for module in ("i915", "xe", "amdgpu", "nvidia", "iwlwifi", "snd_hda_intel", "nvme", "zram"):
            modules[module] = self.exists("sys/module/" + module)
        names = (
            "vm.swappiness",
            "vm.vfs_cache_pressure",
            "vm.dirty_ratio",
            "vm.dirty_background_ratio",
            "vm.dirty_writeback_centisecs",
            "vm.dirty_expire_centisecs",
            "vm.laptop_mode",
            "vm.max_map_count",
            "vm.overcommit_memory",
            "fs.file-max",
            "fs.inotify.max_user_watches",
            "fs.inotify.max_user_instances",
            "fs.inotify.max_queued_events",
            "net.core.somaxconn",
        )
        values = {}
        for name in names:
            values[name] = read_int(self.p("proc/sys/" + name.replace(".", "/")))
        return {"sysctls": values, "modules": modules, "systemd": self.exists("run/systemd/system")}

    def databases(self):
        return {
            "postgresql": self.postgresql(),
            "mysql": self.mysql(),
            "redis": self.redis(),
            "sqlite": self.sqlite(),
        }

    def postgresql(self):
        configs = sorted(glob.glob(str(self.p("etc/postgresql/*/main/postgresql.conf"))))
        if not configs:
            return {"installed": False}
        path = Path(configs[-1])
        version = path.parents[1].name
        values = read_key_values(path)
        include = values.get("include_dir", "").strip().strip("'\"")
        include_path = path.parent / include if include else None
        unit = "postgresql.service"
        if ("postgresql@%s-main.service" % version) in self.services():
            unit = "postgresql@%s-main.service" % version
        service = self.services().get(unit, {})
        return {
            "installed": True,
            "version": version,
            "config": str(path),
            "include_dir": str(include_path) if include_path else None,
            "include_supported": bool(include_path),
            "values": {
                "shared_buffers": values.get("shared_buffers"),
                "effective_cache_size": values.get("effective_cache_size"),
                "max_connections": values.get("max_connections"),
                "work_mem": values.get("work_mem"),
            },
            "unit": unit,
            "active": service.get("active"),
        }

    def mysql(self):
        if not self.exists("etc/mysql") and not self.exists("etc/my.cnf"):
            return {"installed": False}
        include_dirs = []
        for directory in ("etc/mysql/mariadb.conf.d", "etc/mysql/conf.d"):
            if self.exists(directory):
                include_dirs.append(str(self.p(directory)))
        mariadb_unit = self.services().get("mariadb.service", {})
        mysql_unit = self.services().get("mysql.service", {})
        if self.which("mariadbd") or any(item.endswith("mariadb.conf.d") for item in include_dirs):
            product = "mariadb"
            server_binary = "mariadbd" if self.which("mariadbd") else None
            unit = "mariadb.service"
        elif self.which("mysqld") or include_dirs:
            product = "mysql"
            server_binary = "mysqld" if self.which("mysqld") else None
            unit = "mysql.service"
        else:
            product = "unknown"
            server_binary = None
            unit = "mysql.service"
        service = mariadb_unit if unit == "mariadb.service" else mysql_unit
        installed = bool(include_dirs and (server_binary or service.get("exists")))
        version = None
        version_tuple = []
        if server_binary:
            result = self.cmd([server_binary, "--version"], timeout=3)
            if result["ok"]:
                match = re.search(r"Ver\s+([0-9]+\.[0-9]+\.[0-9]+)", result["out"])
                if not match:
                    match = re.search(r"([0-9]+\.[0-9]+\.[0-9]+)", result["out"])
                if match:
                    version = match.group(1)
                    version_tuple = [int(part) for part in version.split(".")]
        validate = None
        if server_binary == "mysqld" and version_tuple >= [8, 0, 0]:
            validate = ["mysqld", "--validate-config"]
        return {
            "installed": installed,
            "product": product,
            "version": version,
            "version_tuple": version_tuple,
            "server_binary": server_binary,
            "include_dirs": include_dirs,
            "unit": unit,
            "validate": validate,
            "active": service.get("active"),
            "service_present": bool(service.get("exists")),
        }

    def redis(self):
        config = self.p("etc/redis/redis.conf")
        if not config.exists():
            return {"installed": False}
        values = {}
        for line in read_text(config).splitlines():
            match = re.match(r"\s*(maxmemory|maxmemory-policy)\s+(.+)", line)
            if match:
                values[match.group(1)] = match.group(2).strip()
        return {
            "installed": True,
            "config": str(config),
            "values": values,
            "unit": "redis-server.service",
            "active": self.services().get("redis-server.service", {}).get("active"),
        }

    def sqlite(self):
        if not self.which("sqlite3"):
            return {"installed": False}
        result = self.cmd(["sqlite3", "--version"], timeout=3)
        return {"installed": result["ok"], "version": result["out"] if result["ok"] else None}

    def tools(self):
        names = (
            "gsettings", "dde-dconfig", "busctl", "systemctl", "sysctl", "sudo",
            "powerprofilesctl", "tuned-adm", "glxinfo", "vainfo", "vulkaninfo",
            "nvidia-smi", "xrandr", "lsblk", "update-initramfs",
            "psql", "mysql", "mariadb", "mysqld", "mariadbd", "sqlite3", "redis-cli",
        )
        return {name: self.which(name) for name in names}

    def metrics(self):
        load = read_text(self.p("proc/loadavg")).split()
        pressure = {}
        for resource in ("cpu", "memory", "io"):
            text = read_text(self.p("proc/pressure/" + resource)).strip()
            if not text:
                continue
            line = next((item for item in text.splitlines() if item.startswith("some ")), text.splitlines()[0])
            item = {}
            for part in line.split():
                if "=" in part:
                    key, value = part.split("=", 1)
                    try:
                        item[key] = float(value)
                    except ValueError:
                        pass
            pressure[resource] = item
        temperatures = []
        for path in sorted(glob.glob(str(self.p("sys/class/thermal/thermal_zone*")))):
            value = (read_int(Path(path) / "temp", 0) or 0) / 1000.0
            if 0 < value < 150:
                temperatures.append(value)
        battery = []
        ac_online = None
        for path in sorted(glob.glob(str(self.p("sys/class/power_supply/*")))):
            supply = Path(path)
            kind = read_text(supply / "type").strip()
            if kind == "Battery":
                battery.append({"capacity": read_int(supply / "capacity"),
                                "status": read_text(supply / "status").strip() or None})
            elif kind == "Mains":
                online = read_text(supply / "online").strip()
                if online in ("0", "1"):
                    ac_online = online == "1"
        info = {}
        for line in read_text(self.p("proc/meminfo")).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                parts = value.split()
                if parts:
                    try:
                        info[key.strip()] = int(parts[0])
                    except ValueError:
                        pass
        return {
            "load1": float(load[0]) if len(load) > 0 else None,
            "load5": float(load[1]) if len(load) > 1 else None,
            "load15": float(load[2]) if len(load) > 2 else None,
            "pressure": pressure,
            "available_mb": (info.get("MemAvailable") or 0) // 1024,
            "swap_free_mb": (info.get("SwapFree") or 0) // 1024,
            "max_temp_c": max(temperatures) if temperatures else None,
            "governor": read_text(self.p("sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")).strip() or None,
            "battery": battery,
            "ac_online": ac_online,
        }

    def capabilities(self):
        uid = os.geteuid()
        sudo = False
        if uid != 0 and self.which("sudo"):
            result = self.cmd(["sudo", "-n", "true"], timeout=3)
            sudo = result["ok"]
        return {
            "uid": uid,
            "root": uid == 0,
            "sudo_noninteractive": sudo,
            "privileged": uid == 0 or sudo,
            "systemd": self.exists("run/systemd/system"),
            "gsettings": self.which("gsettings"),
            "dde": self._schema_exists("com.deepin.dde.power"),
            "display": bool(self.env.get("DISPLAY") or self.env.get("WAYLAND_DISPLAY")),
        }

    # ------------------------------------------------------------ gsettings
    def _schema_exists(self, schema):
        key = ("schema", schema)
        if key not in self._command_cache:
            if not self.which("gsettings"):
                self._command_cache[key] = False
            else:
                result = self.cmd(["gsettings", "list-schemas"], timeout=4)
                self._command_cache[key] = schema in result["out"].split()
        return self._command_cache[key]

    def gsettings_get(self, schema, key):
        if not self.which("gsettings"):
            return None
        result = self.cmd(["gsettings", "get", schema, key], timeout=4)
        return result["out"] if result["ok"] else None

    def gsettings_keys(self, schema):
        if not self.which("gsettings"):
            return []
        result = self.cmd(["gsettings", "list-keys", schema], timeout=4)
        return result["out"].split() if result["ok"] else []


def hardware_hash(machines):
    cpu = machines.get("cpu", {})
    memory = machines.get("memory", {})
    gpu = machines.get("gpu", {})
    host = machines.get("host", {})
    stable = {
        "cpu": [cpu.get("model"), cpu.get("logical"), cpu.get("physical")],
        "memory_mb": memory.get("total_mb"),
        "gpus": sorted(card.get("pci_id") for card in gpu.get("cards", [])),
        "product": host.get("product"),
        "board": host.get("board"),
    }
    return hashlib.sha256(json.dumps(stable, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def classify(machines):
    cpu = machines.get("cpu", {})
    memory = machines.get("memory", {})
    gpu = machines.get("gpu", {})
    storage = machines.get("storage", {})
    power = machines.get("power", {})
    desktop = machines.get("desktop", {})
    displays = gpu.get("display") or []
    max_width = max([item.get("width") or 0 for item in displays] or [0])
    max_refresh = max([item.get("refresh") or 0 for item in displays] or [0])
    models = " ".join(gpu.get("names") or []).lower()
    if "nvidia" in models or any(card.get("driver") in ("nvidia", "nouveau") for card in gpu.get("cards", [])):
        gpu_class = "nvidia"
    elif "amd" in models or any(card.get("driver") == "amdgpu" for card in gpu.get("cards", [])):
        gpu_class = "amd"
    elif "intel" in models or any(card.get("driver") == "i915" for card in gpu.get("cards", [])):
        gpu_class = "intel"
    else:
        gpu_class = "unknown"
    if len(gpu.get("cards", [])) > 1 and gpu_class != "unknown":
        gpu_class = "hybrid-" + gpu_class
    total = memory.get("total_mb") or 0
    memory_class = "low" if total < 8 * 1024 else ("mid" if total <= 16 * 1024 else "high")
    base = storage.get("root_disk") or ""
    transport = "nvme" if base.startswith("nvme") else ("ssd" if storage.get("rotational") == 0 else ("hdd" if storage.get("rotational") == 1 else "unknown"))
    sessions = desktop.get("sessions") or []
    primary_card = next((card for card in gpu.get("cards", []) if card.get("boot_vga")), None)
    if primary_card is None and gpu.get("cards"):
        primary_card = gpu["cards"][0]
    primary_driver = (primary_card or {}).get("driver") or ""
    primary_gpu_class = (
        "intel" if primary_driver in ("i915", "xe") or "intel" in str((primary_card or {}).get("pci_id", ""))
        else "amd" if primary_driver in ("amdgpu", "radeon")
        else "nvidia" if primary_driver in ("nvidia", "nouveau")
        else "unknown"
    )
    return {
        "form_factor": "laptop" if power.get("battery_present") else "desktop",
        "cpu_class": (
            "intel" if "intel" in (cpu.get("vendor") or "").lower()
            else "amd" if "amd" in (cpu.get("vendor") or "").lower()
            else "unknown"
        ) + ("-hybrid" if cpu.get("hybrid") else ""),
        "gpu_class": gpu_class,
        "primary_gpu_class": primary_gpu_class,
        "memory_class": memory_class,
        "storage_class": transport,
        "power_source": "ac" if power.get("ac_online") else ("battery" if power.get("battery_present") else "unknown"),
        "session": desktop.get("current_session"),
        "desktop": desktop.get("current_desktop"),
        "has_wayland_session": any(item.get("type") == "wayland" for item in sessions),
        "has_x11_session": any(item.get("type") == "x11" for item in sessions),
        "display_width": max_width or None,
        "display_refresh": max_refresh or None,
        "databases": [name for name, data in (machines.get("databases") or {}).items() if data.get("installed")],
    }
