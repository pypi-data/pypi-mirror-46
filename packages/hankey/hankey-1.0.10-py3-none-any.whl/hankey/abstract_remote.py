class AbstractCloudClient(object):

    def __init__(self, directory):
        self.dir = directory

    def delete(self, path):
        raise NotImplementedError()

    def mkdir(self, path):
        raise NotImplementedError()

    def exists(self, path):
        raise NotImplementedError()

    def delete_r(self, path):
        raise NotImplementedError()

    def upload(self, filename, path):
        raise NotImplementedError()

    def ls(self, path, types="df"):
        raise NotImplementedError()

    def download(self, path, filename):  # to file
        raise NotImplementedError()
