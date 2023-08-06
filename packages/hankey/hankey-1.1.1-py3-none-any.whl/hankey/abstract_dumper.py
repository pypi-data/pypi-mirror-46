class AbstractDumper(object):
    def __init__(self, name, backups):
        self.name = name
        self.backups = backups

    def get_dump(self, path):
        raise NotImplementedError()

    def restore(self, path):
        raise NotImplementedError()
