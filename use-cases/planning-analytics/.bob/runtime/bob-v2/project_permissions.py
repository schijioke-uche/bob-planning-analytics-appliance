#!/usr/bin/env python3
"""Requested 0777 policy for real paths inside an explicit appliance tree."""
from __future__ import annotations
import os
import stat
from pathlib import Path


def normalize_tree(root: Path) -> int:
    """Set mode 0777, without traversing symbolic links or changing file contents.

    Directories are chmodded before enumeration so owned 0000 paths can be
    repaired. Files created concurrently are picked up by the next maintenance
    pass. OS failures are real failures; no permission-policy warning is emitted.
    """
    root = Path(root)
    if root.is_symlink():
        return 0
    count = 0
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            info = current.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode):
            continue
        if not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)):
            continue
        # Do not chmod a concurrently replaced symbolic link.
        if current.is_symlink():
            continue
        if stat.S_IMODE(info.st_mode) != 0o777:
            os.chmod(current, 0o777, follow_symlinks=False)
        count += 1
        if stat.S_ISDIR(info.st_mode):
            with os.scandir(current) as entries:
                stack.extend(Path(entry.path) for entry in entries
                             if not entry.is_symlink())
    return count
