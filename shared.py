from firebase_admin import db
import click

def read_from_database(path):
    ref = db.reference(path)
    return ref.get()


def add_meeting_to_database(the_data, meeting_id):
    ref = db.reference(f"/Meetings/{meeting_id}")
    ref.set(the_data)


def validate_not_empty(ctx, param, value):
    if not value:
        raise click.BadParameter("Input cannot be empty")
    return value


def list_mentors(mentors):
    for i in range(len(mentors)):
        if i == 0:
            click.secho("Available mentors:", fg="blue")

        key, mentor_data = mentors[i]

        if mentor_data.get("role") == "mentor":
            click.echo(f"\nMentor {i + 1}:")
            click.echo(f'Name: {mentor_data.get("full_name") or mentor_data.get("first_name")}')
            click.echo(f'Email: {mentor_data.get("email")}')
            click.echo(f'Expertise: {mentor_data.get("expertise")}')


def list_workshops():
    data = read_from_database("/Workshops")
    i = 0
    # If user is indeed signed in. List all upcoming workshops
    if "session exists":
        for k,v in data.items():
            if i == 0:
                click.secho(f"\nAvailable workshops:\n", fg="blue")

            click.echo(f"Topic {i + 1} - {v['topic']}")
            i += 1