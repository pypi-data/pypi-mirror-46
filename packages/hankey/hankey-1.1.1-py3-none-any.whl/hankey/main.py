import os
import time

from hankey.cloud_utils import get_cloud
from hankey.utils import get_config, get_jobs, get_dump, restore_dump

PREFIX = ".hankey"


def run(user=None):
    prefix = PREFIX
    conf = get_config(user)
    if not isinstance(conf, dict) or "jobs" not in conf or\
            not isinstance(conf["jobs"], dict) or "remotes" not in conf or not isinstance(conf["remotes"], dict):
        raise Exception("Invalid config file")
    if "prefix" in conf and isinstance(conf["prefix"], str):
        prefix = os.path.join(prefix, conf["prefix"])

    remotes = {}
    for k, remote in conf["remotes"].items():
        if "namespace" not in remote:
            raise Exception("Invalid config file")
        try:
            dir = prefix
            if "dir" in remote:
                dir = os.path.join(dir, prefix)
            remotes[k] = get_cloud(remote["namespace"], dir, remote)
        except:
            raise Exception("Invalid config file")

    for k, obj in conf["jobs"].items():
        if "remote" not in obj or "time" not in obj:
            raise Exception("Invalid config file")
        remote = obj["remote"]
        if remote not in remotes:
            raise Exception("Invalid config file")
        jobs = get_jobs(k, obj)
        r = remotes[remote]
        tm = obj["time"]
        if not isinstance(tm, int):
            raise Exception("Invalid config file")
        r.mkdir(k)
        l = [int(d) for d in r.ls(k)]
        l.sort()
        if not l or time.time() - l[-1] >= tm:
            for job in jobs:
                get_dump(job, r)


def restore(job_name):
    prefix = PREFIX
    conf = get_config()
    if not isinstance(conf, dict) or "jobs" not in conf or \
            not isinstance(conf["jobs"], dict) or "remotes" not in conf or not isinstance(conf["remotes"], dict):
        raise Exception("Invalid config file")
    if "prefix" in conf and isinstance(conf["prefix"], str):
        prefix = os.path.join(prefix, conf["prefix"])

    remotes = {}
    for k, remote in conf["remotes"].items():
        if "namespace" not in remote:
            raise Exception("Invalid config file")
        try:
            dir = prefix
            if "dir" in remote:
                dir = os.path.join(dir, prefix)
            remotes[k] = get_cloud(remote["namespace"], dir, remote)
        except:
            raise Exception("Invalid config file")

    if job_name not in conf["jobs"]:
        raise Exception("No such job: {}".format(job_name))
    k = job_name
    obj = conf["jobs"]
    if "remote" not in obj or "time" not in obj:
        raise Exception("Invalid config file")
    remote = obj["remote"]
    if remote not in remotes:
        raise Exception("Invalid config file")
    jobs = get_jobs(k, obj)
    r = remotes[remote]
    tm = obj["time"]
    if not isinstance(tm, int):
        raise Exception("Invalid config file")
    r.mkdir(k)
    l = [int(d) for d in r.ls(k)]
    l.sort()
    if not l or time.time() - l[-1] >= tm:
        for job in jobs:
            restore_dump(job, r)
