import platform
import sys
import os

def _is_raspberry_pi():
    try:
        with open("/proc/device-tree/model", "r") as f:
            return "raspberry pi" in f.read().lower()
    except FileNotFoundError:
        pass

    try:
        with open("/proc/cpuinfo", "r") as f:
            return "raspberry pi" in f.read().lower()
    except FileNotFoundError:
        pass

    return False


def get_platform():
    system = platform.system().lower()

    if system == "windows":
        return "win"

    if system == "linux":
        if _is_raspberry_pi():
            return "rpi"
        return "linx"

    if system == "darwin":
        return "mac"

    return "unknown"
