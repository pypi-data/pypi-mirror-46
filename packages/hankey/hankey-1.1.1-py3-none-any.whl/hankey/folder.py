import os
from subprocess import call

from hankey.abstract_dumper import AbstractDumper


class FolderDumper(AbstractDumper):
    def __init__(self, name, backups, path):
        self.path = path
        super().__init__(name, backups)

    def get_dump(self, path):
        src = os.path.abspath(self.path)
        dst = os.path.abspath(path)
        if not os.path.exists(src) or not os.path.isdir(src):
            raise Exception("Invalid directory {}".format(src))
        call(['rm', '-rf', dst])
        call(['cp', '-r', src, dst])

    def restore(self, path):
        src = os.path.abspath(self.path)
        dst = os.path.abspath(path)
        call(['rm', '-rf', src])
        call(['cp', '-r', dst, src])
