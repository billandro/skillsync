from firebase_admin import db

def read_from_database(path):
    ref = db.reference(path)
    return ref.get()