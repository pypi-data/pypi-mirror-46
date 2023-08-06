import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

from hankey.abstract_remote import AbstractCloudClient


class FirebaseClient(AbstractCloudClient):
    def __init__(self, directory, cert, sb):
        super().__init__(directory)
        cred = credentials.Certificate(cert)
        self.app = firebase_admin.initialize_app(cred, {
            'storageBucket': sb,
        })
        self.bucket = storage.bucket(app=self.app)

    def mkdir(self, path):
        pass

    def upload(self, filename, path):
        blob = self.bucket.blob(os.path.join(self.dir, path))
        blob.upload_from_filename(filename)

    def exists(self, path):
        blob = self.bucket.get_blob(os.path.join(self.dir, path))
        return blob.exists()

    def delete(self, path):
        blob = self.bucket.get_blob(os.path.join(self.dir, path))
        if blob.exists():
            blob.delete()
            return True
        return False

    def delete_r(self, path):
        for b in self.bucket.list_blobs(prefix=os.path.join(self.dir, path)):
            b.delete()

    def ls(self, path, types="df"):
        prefix = os.path.join(self.dir, path)
        if not prefix.endswith('/'):
            prefix += '/'
        res = set()
        for b in self.bucket.list_blobs(prefix=prefix):
            name = b.name[len(prefix):]
            if '/' in name:
                if 'd' in types:
                    res.add(name[:name.find('/')])
            else:
                if 'f' in types:
                    res.add(name)
        return list(res)

    def download(self, path, filename):
        blob = self.bucket.get_blob(os.path.join(self.dir, path))
        if blob.exists():
            blob.download_to_filename(filename)
            return True
        return False
