"""Behavioural tests for pymount's Manager path/lookup helpers.

Manager.__init__ reads /proc/partitions and /proc/mounts, so these tests
build an instance with object.__new__ and populate only the state each
pure helper touches, keeping the tests independent of the host's disks.
"""

import io
import unittest
from unittest.mock import patch

import pytest

from pymount import mgr


def _manager(mounts: str = "") -> mgr.Manager:
    """A Manager built from fake /proc/partitions and /proc/mounts contents."""
    files = {
        "/proc/partitions": "major minor  #blocks  name\n\n",
        "/proc/mounts": mounts,
    }

    def fake_open(path):
        return io.StringIO(files[path])

    with patch("builtins.open", side_effect=fake_open):
        return mgr.Manager()


class DeviceNameTests(unittest.TestCase):
    def test_get_device_name_strips_dev_prefix(self):
        assert mgr.Manager.get_device_name("/dev/sda") == "sda"

    def test_get_device_block_path(self):
        manager = _manager()
        assert manager.get_device_block_path("/dev/sdb") == "/sys/block/sdb"

    def test_get_media_path(self):
        manager = _manager()
        assert manager.get_media_path("/dev/sdc") == "/media/sdc"


class MountLookupTests(unittest.TestCase):
    def test_is_mounted_true_and_false(self):
        manager = _manager("/dev/sda1 /media/usb ext4 rw 0 0\n")
        assert manager.is_mounted("/dev/sda1")
        assert not manager.is_mounted("/dev/sdz9")

    def test_get_mount_point_returns_stored_path(self):
        manager = _manager("/dev/sda1 /media/usb ext4 rw 0 0\n")
        assert manager.get_mount_point("/dev/sda1") == "/media/usb"

    def test_get_mount_point_missing_raises(self):
        manager = _manager()
        with pytest.raises(KeyError):
            manager.get_mount_point("/dev/nope")


if __name__ == "__main__":
    unittest.main()
