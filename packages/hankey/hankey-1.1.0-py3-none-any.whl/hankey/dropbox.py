import os

import dropbox
from dropbox.files import FolderMetadata, FileMetadata

from hankey.abstract_remote import AbstractCloudClient


class DropBoxClient(AbstractCloudClient):

    def __init__(self, directory, token):
        super().__init__(directory)
        if directory and not directory.startswith('/'):
            directory = "/" + directory
        self.dir = directory
        self.dbx = dropbox.Dropbox(token)
        self.mkdir('')

    def exists(self, path):
        path = os.path.join(self.dir, path)
        if path.endswith('/'):
            path = path[:-1]
        try:
            self.dbx.files_get_metadata(path)
            return True
        except:
            return False

    def mkdir(self, path):
        if self.exists(path):
            return
        path = os.path.join(self.dir, path)
        if path.endswith('/'):
            path = path[:-1]
        self.dbx.files_create_folder_v2(path)

    def delete(self, path):
        self.dbx.files_delete_v2(os.path.join(self.dir, path))

    def delete_r(self, path):
        self.dbx.files_delete_v2(os.path.join(self.dir, path))

    def upload(self, filename, path):
        with open(filename, 'rb') as f:
            self.dbx.files_upload(f.read(), os.path.join(self.dir, path))

    def ls(self, path, types="df"):
        res = []
        for entry in self.dbx.files_list_folder(os.path.join(self.dir, path)).entries:
            if isinstance(entry, FolderMetadata) and 'd' in types:
                res.append(entry.name)
            elif isinstance(entry, FileMetadata) and 'f' in types:
                res.append(entry.name)
        return res

    def download(self, path, filename):
        self.dbx.files_download_to_file(filename, os.path.join(self.dir, path))
