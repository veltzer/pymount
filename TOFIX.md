# TOFIX

Findings from a code scan on 2026-10-04.

## High

- `src/pymount/mgr.py:75` and `src/pymount/mgr.py:85` - `mount_partition`/`unmount_partition` call `self.is_mounted(path)` with the mount point (`/media/<name>`), but `_mounted_devices` (line 46) is keyed by device, so the check is always `False`: `unmount_partition` never unmounts anything, and `mount_partition` always runs `os.mkdir` + `mount`, raising `FileExistsError` when the directory already exists. Check membership in `self._mounted_devices.values()` (or key a second dict by mount point), and refresh the mount table after each `mount`/`umount` - `_get_mounts` is only called once in `__init__` (line 14), so the state is stale after any change.

## Medium

- `src/pymount/mgr.py:135` - `print_me` reports `is_mounted(device)` for the whole-disk device (`/dev/sdb`), but what gets mounted is the partition returned by `get_partition` (`/dev/sdb1`), so it always prints `Mounted: False`; report the partition's state.
- `src/pymount/mgr.py:65-71` - `get_partition` takes the first word of the second-to-last line of `fdisk -l` output, which breaks when fdisk prints a trailing note (e.g. "Partition table entries are not in disk order") or the disk has no partition table; use `lsblk -J -o NAME,TYPE <device>` and pick the `part` entries.
- `pyproject.toml:88` - the mypy override applies `ignore_missing_imports = true` to `pymount.*`, the package itself, under a comment saying the list is for third-party libraries without stubs; remove the entry so a broken internal import is reported.

## Low

- `src/pymount/mgr.py:76,90` - `mount_partition` creates `/media/<name>` but `unmount_partition` never removes it (the cleanup is a commented-out `os.system("rm -rf " + path)`); replace with `os.rmdir(path)` after a successful `umount` and delete the commented code.
- `src/pymount/mgr.py:33` - USB disk detection assumes `minor % 16 == 0` marks a whole disk, which is only true for SCSI/sd devices (major 8, per the comment at line 17); NVMe/MMC USB adapters are missed. Use `/sys/class/block/<dev>/partition` (absent for whole disks) instead.
- `tests/unit_tests/test_mgr.py:16-17,37,43` - `# pylint: disable=protected-access` comments, but pylint is not part of the build (not in the dev group or `rsconstruct.toml`); remove them.
- `doc/TODO.txt` - empty file; delete it.
