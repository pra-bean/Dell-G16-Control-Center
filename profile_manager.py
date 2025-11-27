import subprocess
from performance import (
    set_platform_profile,
    set_cpu_governor
)

# -------------------------
# QUIET MODE
# -------------------------

def apply_quiet():
    """
    Lowest noise + lowest power usage.
    """
    set_platform_profile("quiet")
    set_cpu_governor("powersave")  # slowest + coolest
    return "Quiet mode applied."


# -------------------------
# BALANCED MODE
# -------------------------

def apply_balanced():
    """
    Normal daily use.
    """
    set_platform_profile("balanced")
    set_cpu_governor("powersave")  # adaptive governor
    return "Balanced mode applied."


# -------------------------
# PERFORMANCE MODE
# -------------------------

def apply_performance():
    """
    High performance for CPU-bound workloads.
    """
    set_platform_profile("performance")
    set_cpu_governor("performance")
    return "Performance mode applied."


# -------------------------
# G-MODE
# -------------------------

def apply_g_mode():
    """
    Dell G-Mode equivalent:
    - platform profile: performance
    - CPU governor: performance
    - Nvidia: unlock max perf mode (if GPU is allowed)
    """
    set_platform_profile("performance")
    set_cpu_governor("performance")

    # Enable NVIDIA persistence mode (safe)
    try:
        subprocess.run(["nvidia-smi", "-pm", "1"], check=False)
    except:
        pass

    # Unlock GPU clocks (safe: it only uses factory-supported clocks)
    try:
        # Query supported clock speeds
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=clocks.max.gr,clocks.max.memory",
             "--format=csv,noheader,nounits"],
            text=True
        ).strip()

        max_graphics, max_memory = out.split(",")

        # Apply max GPU frequencies
        subprocess.run(
            ["nvidia-smi", "-ac", f"{max_memory.strip()},{max_graphics.strip()}"],
            check=False
        )

    except:
        pass

    return "G-Mode applied (Performance + GPU Boost)."
