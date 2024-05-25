import os
import subprocess
from typing import List, Dict


class Manager:
    def __init__(self):
        self._devices: List[str] = []
        self._mounted_devices: Dict[str, str] = {}
        self._get_media_devices()
        self._get_mounts()

    def _get_media_devices(self):
        # If the major number is 8, that indicates it to be a disk device.
        #
        # The minor number is the partitions on the same device:
        # - 0 means the entire disk
        # - 1 is the primary
        # - 2 is extended
        # - 5 is logical partitions
        # The maximum number of partitions is 15.
        #
        # Use `$ sudo fdisk -l` and `$ sudo sfdisk -l /dev/sda` for more information.
        with open("/proc/partitions", "rt") as f:
            for line in f.readlines()[2:]:  # skip header lines
                words = [word.strip() for word in line.split()]
                minor_number = int(words[1])
                device_name = words[3]

                if (minor_number % 16) == 0:
                    path = "/sys/class/block/" + device_name

                    if os.path.islink(path):
                        if os.path.realpath(path).find("/usb") > 0:
                            self._devices.append("/dev/" + device_name)

    def _get_mounts(self):
        with open("/proc/mounts", "rt") as file_handle:
            for line in file_handle:
                line = line.rstrip()
                parts = line.split(" ")
                part_device = parts[0]
                part_mount_point = parts[1]
                self._mounted_devices[part_device] = part_mount_point

    def is_mounted(self, device):
        return device in self._mounted_devices

    def get_mount_point(self, device):
        return self._mounted_devices[device]

    @staticmethod
    def get_device_name(device):
        return os.path.basename(device)

    def get_device_block_path(self, device):
        return f"/sys/block/{self.get_device_name(device)}"

    def get_media_path(self, device):
        return "/media/" + self.get_device_name(device)

    @staticmethod
    def get_partition(device):
        output = subprocess.check_output([
            "fdisk",
            "-l",
            device
        ]).decode()
        return output.split("\n")[-2].split()[0].strip()

    def mount_partition(self, partition, name="usb"):
        path = self.get_media_path(name)
        if not self.is_mounted(path):
            os.mkdir(path)
            subprocess.check_call([
                "mount",
                partition,
                path,
            ])

    def unmount_partition(self, name="usb"):
        path = self.get_media_path(name)
        if self.is_mounted(path):
            subprocess.check_call([
                "umount",
                path,
            ])
            # os.system("rm -rf " + path)

    def mount(self, device, name=None):
        if not name:
            name = self.get_device_name(device)
        self.mount_partition(self.get_partition(device), name)

    def unmount(self, device, name=None):
        if not name:
            name = self.get_device_name(device)
        self.unmount_partition(name)

    def is_removable(self, device):
        path = self.get_device_block_path(device) + "/removable"
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read().strip() == "1"
        return None

    def get_size(self, device):
        path = self.get_device_block_path(device) + "/size"
        if os.path.exists(path):
            with open(path, "r") as f:
                # Multiply by 512, as Linux sectors are always considered to be 512 bytes long
                return int(f.read().strip()) * 512
        return -1

    def get_model(self, device):
        path = self.get_device_block_path(device) + "/device/model"
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read().strip()
        return None

    def get_vendor(self, device):
        path = self.get_device_block_path(device) + "/device/vendor"
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read().strip()
        return None

    def print_me(self):
        for device in self._devices:
            self.mount(device)
            print(f"Drive: {self.get_device_name(device)}")
            print(f"Mounted: {self.is_mounted(device)}")
            print(f"Removable: {self.is_removable(device)}")
            print(f"Size: {self.get_size(device)} bytes")
            size = self.get_size(device) / 1024 ** 3
            print(f"Size: {size:.2f}")
            print(f"Model: {self.get_model(device)}")
            print(f"Vendor: {self.get_vendor(device)}")
            self.unmount(device)
