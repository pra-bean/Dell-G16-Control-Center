from pathlib import Path
import glob

# --- PLATFORM PROFILE CONTROL ---
# Uses: /sys/firmware/acpi/platform_profile

PROFILE_PATH = Path("/sys/firmware/acpi/platform_profile")


def get_platform_profile():
    if PROFILE_PATH.exists():
        return PROFILE_PATH.read_text().strip()
    return None


def set_platform_profile(mode: str):
    """
    mode must be: quiet, balanced, performance
    Must run with sudo.
    """
    if not PROFILE_PATH.exists():
        return False

    try:
        PROFILE_PATH.write_text(mode)
        return True
    except PermissionError:
        return False


# --- CPU GOVERNOR CONTROL ---
# Uses: /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

def get_governors():
    result = {}
    paths = glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")

    for p in paths:
        cpu = p.split("/")[-2]
        try:
            result[cpu] = Path(p).read_text().strip()
        except:
            result[cpu] = None

    return result


def set_cpu_governor(gov: str):
    """
    gov must be: powersave, schedutil, performance
    Must run with sudo.
    """
    paths = glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
    success = True

    for p in paths:
        try:
            Path(p).write_text(gov)
        except PermissionError:
            success = False

    return success
