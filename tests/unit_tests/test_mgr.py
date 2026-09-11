"""Behavioural tests for pymount's Manager path/lookup helpers.

Manager.__init__ reads /proc/partitions and /proc/mounts, so these tests
build an instance with object.__new__ and populate only the state each
pure helper touches, keeping the tests independent of the host's disks.
"""

import unittest

from pymount import mgr


def _bare_manager() -> mgr.Manager:
    """A Manager without the /proc-reading __init__ side effects."""
    instance = object.__new__(mgr.Manager)
    instance._devices = []  # pylint: disable=protected-access
    instance._mounted_devices = {}  # pylint: disable=protected-access
    return instance


class DeviceNameTests(unittest.TestCase):
    def test_get_device_name_strips_dev_prefix(self):
        self.assertEqual(mgr.Manager.get_device_name("/dev/sda"), "sda")

    def test_get_device_block_path(self):
        manager = _bare_manager()
        self.assertEqual(manager.get_device_block_path("/dev/sdb"), "/sys/block/sdb")

    def test_get_media_path(self):
        manager = _bare_manager()
        self.assertEqual(manager.get_media_path("/dev/sdc"), "/media/sdc")


class MountLookupTests(unittest.TestCase):
    def test_is_mounted_true_and_false(self):
        manager = _bare_manager()
        manager._mounted_devices = {"/dev/sda1": "/media/usb"}  # pylint: disable=protected-access
        self.assertTrue(manager.is_mounted("/dev/sda1"))
        self.assertFalse(manager.is_mounted("/dev/sdz9"))

    def test_get_mount_point_returns_stored_path(self):
        manager = _bare_manager()
        manager._mounted_devices = {"/dev/sda1": "/media/usb"}  # pylint: disable=protected-access
        self.assertEqual(manager.get_mount_point("/dev/sda1"), "/media/usb")

    def test_get_mount_point_missing_raises(self):
        manager = _bare_manager()
        with self.assertRaises(KeyError):
            manager.get_mount_point("/dev/nope")


if __name__ == "__main__":
    unittest.main()
