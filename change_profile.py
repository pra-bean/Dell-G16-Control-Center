#!/usr/bin/env python3
import sys
from profile_manager import (
    apply_quiet,
    apply_balanced,
    apply_performance,
    apply_g_mode
)

if len(sys.argv) != 2:
    print("Usage: change_profile.py <quiet|balanced|performance|gmode>")
    sys.exit(1)

mode = sys.argv[1].lower()

if mode == "quiet":
    print(apply_quiet())
elif mode == "balanced":
    print(apply_balanced())
elif mode == "performance":
    print(apply_performance())
elif mode == "gmode":
    print(apply_g_mode())
else:
    print("Invalid mode")
    sys.exit(1)
