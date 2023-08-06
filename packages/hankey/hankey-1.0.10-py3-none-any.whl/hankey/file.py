import os
from shutil import copyfile

from hankey.abstract_dumper import AbstractDumper


class FileDumper(AbstractDumper):
    def __init__(self, name, backups, path):
        self.path = path
        super().__init__(name, backups)

    @property
    def filename(self):
        rp = self.path[::-1]
        if '/' in rp:
            rp = rp[:rp.find('/')]
        return rp[::-1]

    def get_dump(self, path):
        src = os.path.abspath(self.path)
        dst = os.path.abspath(os.path.join(path, self.filename))
        if not os.path.exists(src) or not os.path.isfile(src):
            raise Exception("Invalid file {}".format(src))
        copyfile(src, dst)

    def restore(self, path):
        src = os.path.abspath(self.path)
        dst = os.path.abspath(os.path.join(path, self.filename))
        copyfile(dst, src)
