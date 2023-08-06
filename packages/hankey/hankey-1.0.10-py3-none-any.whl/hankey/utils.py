import hashlib
import json
import os
import time
from subprocess import call

from hankey.command import CommandDumper
from hankey.file import FileDumper
from hankey.folder import FolderDumper
from hankey.tmp import tmp_dir


def get_config(user=None):
    try:
        if user:
            path = '/home/{}/.hankey/config.json'.format(user)
        else:
            path = os.path.expanduser('~/.hankey/config.json')
        with open(path, 'r') as f:
            return json.load(f)
    except:
        raise Exception("config file is is either not present or invalid")


def get_jobs(name, obj: dict):
    if "type" not in obj:
        raise Exception("Invalid config")
    if "backups" not in obj or not isinstance(obj["backups"], int):
        raise Exception("Invalid config")
    backups = obj["backups"]
    t = obj["type"]
    if t == "file":
        if "path" not in obj:
            raise Exception("Invalid config")
        return [FileDumper(name, backups, obj["path"])]
    if t == "folder":
        if "path" not in obj:
            raise Exception("Invalid config")
        return [FolderDumper(name, backups, obj["path"])]
    if t == "command":
        if "load" not in obj or "dump" not in obj:
            raise Exception("Invalid config")
        return [CommandDumper(name, backups, obj["dump"], obj["load"])]
    raise Exception("Invalid config")


def get_file_hash(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_dir_hash(path):
    path = os.path.abspath(path)
    if os.path.isfile(path):
        return get_file_hash(path)
    sha256_hash = hashlib.sha256()
    for d in os.listdir(path):
        p = os.path.join(path, d)
        t = 'd' if os.path.isdir(p) else 'f'
        sha256_hash.update(hashlib.sha3_256((t + '$' + d + '$' + get_dir_hash(p)).encode()).digest())
    return sha256_hash.hexdigest()


def remove_empty_folders(path):
    path = os.path.abspath(path)
    if os.path.isfile(path):
        return True
    flag = False
    for d in os.listdir(path):
        p = os.path.join(path, d)
        if not remove_empty_folders(p):
            call(['rm', '-rf', p])
        else:
            flag = True
    return flag


def get_remote_hash(remote, job):
    l = [int(d) for d in remote.ls(job.name)]
    l.sort()
    if not l:
        return None
    latest = os.path.join(job.name, str(l[-1]))
    hl = os.path.join(latest, '.hash.hnk')
    with tmp_dir() as td:
        dst = os.path.join(td, '.hash.hnk')
        remote.download(hl, dst)
        with open(dst, 'r+') as fr:
            h = fr.read().strip()
    return h


def get_dump(job, remote):
    remote.mkdir(job.name)
    with tmp_dir() as td:
        ts = str(int(time.time()))
        job.get_dump(td)
        remove_empty_folders(td)
        dh = get_dir_hash(td)
        rh = get_remote_hash(remote, job)
        if dh != rh:
            remote.mkdir(os.path.join(job.name, ts))
            with open(os.path.join(td, '.hash.hnk'), 'w+') as fw:
                fw.write(dh)
            if remote.exists(ts):
                remote.delete_r(ts)

            stack = [(td, os.path.join(job.name, ts))]
            while stack:
                local_path, remote_path = stack.pop()
                for d in os.listdir(local_path):
                    lp = os.path.join(local_path, d)
                    rp = os.path.join(remote_path, d)
                    if os.path.isfile(lp):
                        remote.upload(lp, rp)
                    else:
                        stack.append((lp, rp))
        l = [int(d) for d in remote.ls(job.name)]
        l.sort()
        while len(l) > job.backups:
            remote.delete_r(os.path.join(job.name, str(l[0])))
            l = l[1:]


def restore_dump(job, remote):
    remote.mkdir(job.name)
    l = [int(d) for d in remote.ls(job.name)]
    l.sort()
    if not l:
        raise Exception("No backups found")
    ts = str(l[-1])
    with tmp_dir() as td:
        stack = [(td, os.path.join(job.name, ts))]
        while stack:
            local_path, remote_path = stack.pop()
            for d in remote.ls(remote_path, 'd'):
                lp = os.path.join(local_path, d)
                rp = os.path.join(remote_path, d)
                call(['mkdir', '-p', lp])
                stack.append((lp, rp))
            for d in remote.ls(remote_path, 'f'):
                lp = os.path.join(local_path, d)
                rp = os.path.join(remote_path, d)
                remote.download(rp, lp)
        call(['rm', '-rf', os.path.join(td, '.hash.hnk')])
        job.restore(td)

