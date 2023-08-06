import os
from subprocess import call

from hankey.abstract_dumper import AbstractDumper


class ScriptDumper(AbstractDumper):
    def __init__(self, name, backups, dump_path, load_path):
        self.dump_path = dump_path
        self.load_path = load_path
        super().__init__(name, backups)

    def get_dump(self, path):
        cmd = os.path.abspath(self.dump_path)
        dst = os.path.abspath(path)
        if not os.path.exists(cmd) or not os.path.isfile(cmd):
            raise Exception("Invalid file {}".format(cmd))
        call([cmd, dst])

    def restore(self, path):
        cmd = os.path.abspath(self.load_path)
        dst = os.path.abspath(path)
        if not os.path.exists(cmd) or not os.path.isfile(cmd):
            raise Exception("Invalid file {}".format(cmd))
        call([cmd, dst])
