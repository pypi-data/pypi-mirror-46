from hankey.dropbox import DropBoxClient
from hankey.firebase import FirebaseClient


def get_cloud(namespace, directory, obj):
    if namespace == "firebase":
        if 'storageBucket' not in obj or 'certificate' not in obj:
            raise Exception("invalid config")
        return FirebaseClient(directory, obj['certificate'], obj['storageBucket'])
    if namespace == "dropbox":
        if 'accessToken' not in obj:
            raise Exception("invalid config")
        return DropBoxClient(directory, obj['accessToken'])
    raise Exception("invalid namespace {}".format(namespace))
