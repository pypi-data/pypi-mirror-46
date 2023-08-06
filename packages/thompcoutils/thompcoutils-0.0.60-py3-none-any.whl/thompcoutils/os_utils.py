import os
from thompcoutils.log_utils import get_logger
import psutil
from sys import platform
import time
from netifaces import interfaces, ifaddresses, AF_INET


class UnhandledOs(Exception):
    pass


def _list_zones(walk_dir):
    d = {"timezones": []}
    files = os.listdir(walk_dir)
    for f in files:
        if os.path.isdir(os.path.join(walk_dir, f)):
            d[f] = _list_zones(os.path.join(walk_dir, f))
        else:
            d["timezones"].append(f)
    return d


def list_timezones():
    ost = os_type()
    if ost == "windows":
        time_zones = _list_zones("d:/temp/zoneinfo")
        time_zones["current_timezone"] = get_timezone()
        return time_zones
    elif ost == "linux" or ost == "osx":
        time_zones = _list_zones("/usr/share/zoneinfo")
        time_zones["current_timezone"] = get_timezone()
        return time_zones
    else:
        raise UnhandledOs("{} os not supported".format(ost))


def get_timezone():
    ost = os_type()
    if ost == "linux":
        with open("/etc/timezone") as f:
            return f.read().strip()
    elif ost == "windows" or ost == "osx":
        return time.tzname[0]
    else:
        raise UnhandledOs("{} os not supported".format(ost))


def kill_process(name):
    logger = get_logger()
    logger.info("killing process {}".format(name))
    ost = os_type()
    command = "sudo killall -9 {}".format(name)
    if ost == "linux":
        os.system(command)
    else:
        raise UnhandledOs("{} os not supported.  Linux command would look like {}".format(ost, command))


def is_running(name):
    pid_list = psutil.pids()
    for pid in pid_list:
        # noinspection PyBroadException
        try:
            process = psutil.Process(pid)
            if name == process.name():
                return True
        except Exception:
            pass
    return False


class OSType(enumerate):
    Linux = "Linux"
    OSX = "OSX"
    WINDOWS = "Windows"


def os_type():
    if platform == "linux" or platform == "linux2":
        return OSType.Linux
    elif platform == "darwin":
        return OSType.OSX
    elif platform == "win32":
        return OSType.WINDOWS
    else:
        raise UnhandledOs("Unknown system")


def get_ip_addresses():
    addresses = None
    for interface_name in interfaces():
        addresses = [i['addr'] for i in ifaddresses(interface_name).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
    return addresses
