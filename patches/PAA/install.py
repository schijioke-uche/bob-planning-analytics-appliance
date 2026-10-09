#!/usr/bin/env python3
"""PAA-3.0.0 complete-release maintenance. Python 3.9+, POSIX.

No local content hashes, baseline receipts, permission admission tests or
permission-warning prompts. Preserve every existing regular file on --apply.
Install only missing package files; normalize the entire selected use-case tree.
No network, Bob inference, Git, ownership or external product operations.
"""
from __future__ import annotations
import argparse
import datetime
import fcntl
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import sys
import tempfile
import uuid
import zipfile

HERE = Path(__file__).resolve().parent
RELEASE = 'PAA-3.0.0'
MAX_EXPANDED = 64 * 1024 * 1024

class MaintenanceError(Exception):
    pass


def real_path(path: Path) -> Path:
    """Avoid crossing a symlink below the explicitly selected repository."""
    path = path.expanduser().absolute()
    if '..' in path.parts:
        raise MaintenanceError('Use an explicit path without parent traversal.')
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        if current.is_symlink():
            raise MaintenanceError('Target path is a symbolic link: ' + str(current))
    return path


def normalize_tree(root: Path) -> int:
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
        if current.is_symlink():
            continue
        if stat.S_IMODE(info.st_mode) != 0o777:
            os.chmod(current, 0o777, follow_symlinks=False)
        count += 1
        if stat.S_ISDIR(info.st_mode):
            with os.scandir(current) as entries:
                stack.extend(Path(e.path) for e in entries if not e.is_symlink())
    return count


def select_tree(root: Path, explicit: str | None) -> Path:
    if explicit:
        return real_path(root / explicit)
    for name in ('use-cases', 'use-case'):
        if (root/name).is_dir():
            return real_path(root/name)
    return real_path(root/'use-cases')


def inspect_payload() -> list[tuple[str, bytes]]:
    """Validate archive paths/types/CRC only; there is no baseline manifest."""
    archive = HERE/'payload/planning-analytics.zip'
    if not archive.is_file():
        raise MaintenanceError('Fresh installation needs patches/PAA/payload/planning-analytics.zip.')
    result = []
    seen = set()
    total = 0
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            value = info.filename
            path = PurePosixPath(value)
            if (not value or '\\' in value or path.is_absolute()
                or any(x in ('', '.', '..') for x in value.split('/'))
                or any(ord(x) < 32 for x in value)):
                raise MaintenanceError('Invalid path in release archive.')
            if info.is_dir() or stat.S_IFMT(info.external_attr >> 16) not in (0, stat.S_IFREG):
                raise MaintenanceError('Release archive must contain regular files only.')
            if value in seen:
                raise MaintenanceError('Duplicate path in release archive.')
            seen.add(value)
            total += info.file_size
            if total > MAX_EXPANDED or info.file_size > 16*1024*1024:
                raise MaintenanceError('Release archive is too large.')
            result.append((value, z.read(info)))
    if not any(name == 'xLaunchpad.sh' for name, _ in result):
        raise MaintenanceError('Release archive has no launchpad.')
    return result


def fill_missing(target: Path, members: list[tuple[str, bytes]]) -> tuple[int, int]:
    """Adopt an edited project without replacing .env, templates, code or rules."""
    created = []
    preserved = 0
    try:
        for name, data in members:
            p = target / name
            # Existing symlinks/files are retained but never followed by the writer.
            current = target
            linked = False
            for part in Path(name).parts:
                current /= part
                if current.is_symlink():
                    linked = True
                    break
            if linked or p.exists():
                preserved += 1
                continue
            p.parent.mkdir(parents=True, exist_ok=True)
            try:
                fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                             getattr(os, 'O_NOFOLLOW', 0), 0o777)
            except FileExistsError:
                preserved += 1
                continue
            created.append(p)
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
                os.fchmod(stream.fileno(), 0o777)
        return len(created), preserved
    except BaseException:
        # Roll back only files created by this invocation. Existing work is never touched.
        for p in reversed(created):
            if p.is_file() and not p.is_symlink():
                p.unlink()
        raise


def report(status: str, **details) -> None:
    print(json.dumps(dict(release=RELEASE, status=status,
                          local_baseline_checks=False,
                          permission_admission_checks=False,
                          **details), indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(HERE.parents[1]))
    parser.add_argument('--use-case-dir', choices=('use-cases', 'use-case'))
    action = parser.add_mutually_exclusive_group()
    for name in ('check', 'apply', 'status', 'rollback'):
        action.add_argument('--'+name, action='store_true')
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        raise MaintenanceError('Repository directory does not exist: ' + str(root))
    tree = select_tree(root, args.use_case_dir)
    target = real_path(tree/'planning-analytics')
    present = target.is_dir()
    if args.check:
        if not present:
            inspect_payload()
        report('READY', target=str(target), existing_appliance=present,
               next_action='preserve local files; install missing files; set selected tree to 0777', writes=0)
        return 0
    if args.status:
        report('PRESENT' if present else 'NOT_INSTALLED', target=str(target),
               writes=0, runtime_validation='not performed')
        return 0 if present else 3
    if args.rollback:
        if not present:
            report('NOT_INSTALLED', target=str(target), writes=0)
            return 0
        lock = target/'.bob/runtime/bob-v2/.session.lock'
        # A real live session cannot be moved out from under the running process.
        handle = lock.open('r') if lock.is_file() and not lock.is_symlink() else None
        try:
            if handle:
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError as exc:
                    raise MaintenanceError('Close the running PAA session before archiving it.') from exc
            token = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
            archive = real_path(root/'patches/PAA/rollback-archives'/token)
            archive.mkdir(parents=True, exist_ok=False)
            os.rename(target, archive/'planning-analytics')
            normalize_tree(archive)
            report('ARCHIVED', archive=str(archive/'planning-analytics'), files_deleted=0)
        finally:
            if handle:
                handle.close()
        return 0
    # Default action: one maintenance pass, not repeated check/apply/status calls.
    tree.mkdir(parents=True, exist_ok=True)
    normalize_tree(tree)
    members = inspect_payload() if not present else []
    # An existing complete project does not depend on the old distribution payload.
    # When this release's payload is available, fill absent files only.
    if present and (HERE/'payload/planning-analytics.zip').is_file():
        members = inspect_payload()
    if present:
        created, preserved = fill_missing(target, members)
    else:
        stage = Path(tempfile.mkdtemp(prefix='.paa-install-', dir=tree))
        try:
            created, preserved = fill_missing(stage, members)
            normalize_tree(stage)
            if target.exists() or target.is_symlink():
                raise MaintenanceError('Target appeared during installation; existing files were not changed.')
            os.rename(stage, target)
        finally:
            if stage.exists():
                shutil.rmtree(stage)
    normalized = normalize_tree(tree)
    report('MAINTAINED' if present else 'INSTALLED', target=str(target),
           created_files=created, preserved_files=preserved,
           permission_tree=str(tree), mode='0777', normalized_entries=normalized,
           local_files_replaced=0, sibling_contents_changed=0)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (MaintenanceError, OSError, ValueError, zipfile.BadZipFile) as exc:
        print('PAA maintenance error: '+str(exc), file=sys.stderr)
        sys.exit(2)
