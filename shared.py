from firebase_admin import db
import click

def read_from_database(path):
    ref = db.reference(path)
    return ref.get()


def add_to_database(the_data, meeting_id):
    ref = db.reference(f"/Meetings/{meeting_id}")
    ref.set(the_data)


def validate_not_empty(ctx, param, value):
    if not value:
        raise click.BadParameter("Input cannot be empty")
    return value