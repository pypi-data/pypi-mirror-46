from google.cloud import firestore_v1 as firestore


class Firestore:
    def __init__(self):
        self.fs_client = firestore.Client()
