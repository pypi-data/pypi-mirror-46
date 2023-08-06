import uuid
from subprocess import call


class TmpDir(object):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        call(['rm', '-rf', '/tmp/{}'.format(self.name)])
        call(['mkdir', '-p', '/tmp/{}'.format(self.name)])
        return '/tmp/{}'.format(self.name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        call(['rm', '-rf', '/tmp/{}'.format(self.name)])


def tmp_dir():
    return TmpDir(str(uuid.uuid4()))
