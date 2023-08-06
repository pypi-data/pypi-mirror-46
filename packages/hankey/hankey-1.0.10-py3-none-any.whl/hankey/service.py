import getpass
from subprocess import call

from hankey.tmp import tmp_dir

SERVICE_CODE = """[Unit]
Description=MR Hankey The Chirstmas Poo

[Service]
ExecStart={} {}
StandardOutput=journal+console
StandardError=journal+console
Restart=always

[Install]
WantedBy=multi-user.target

"""


def main():
    with tmp_dir() as td:
        with open('{}/out'.format(td), 'w+') as f:
            call(['which', 'run-hankey'], stdout=f)
        with open('{}/out'.format(td), 'r+') as f:
            run_path = f.read().strip()
        with open('{}/service'.format(td), 'w+') as f:
            f.write(SERVICE_CODE.format(run_path, getpass.getuser()))
        call(["sudo", "cp", '{}/service'.format(td), "/etc/systemd/system/hankey.service"])

    call(["sudo", "systemctl", "start", "hankey.service"])
    call(["sudo", "systemctl", "enable", "hankey.service"])

