import psutil
import subprocess

def get_cpu_stats():
    temps = psutil.sensors_temperatures()
    cpu_temp = None

    # Prefer Intel coretemp
    if "coretemp" in temps:
        cpu_temp = temps["coretemp"][0].current

    usage = psutil.cpu_percent(interval=0.7)
    return {
        "temp": cpu_temp,
        "usage": usage
    }


def get_gpu_stats():
    try:
        out = subprocess.check_output([
            "nvidia-smi",
            "--query-gpu=temperature.gpu,utilization.gpu,clocks.gr",
            "--format=csv,noheader,nounits"
        ], text=True).strip()

        temp, usage, clock = out.split(",")
        return {
            "temp": float(temp),
            "usage": float(usage),
            "clock": float(clock)
        }

    except Exception:
        return {
            "temp": None,
            "usage": None,
            "clock": None
        }


def get_fan_rpm():
    """
    Read fan RPM from dell_smm-virtual hwmon.
    This is READ-ONLY. Your model supports this.
    """
    result = {}

    try:
        out = subprocess.check_output(["sensors"], text=True)
        for line in out.splitlines():
            line = line.strip().lower()
            if "fan" in line and "rpm" in line:
                parts = line.split()
                for p in parts:
                    if p.isdigit():
                        rpm = int(p)
                        name = parts[0].rstrip(":")
                        result[name] = rpm
                        break
    except Exception:
        pass

    return result
