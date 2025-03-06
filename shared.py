from firebase_admin import db
import click, string, random

def read_from_database(path):
    ref = db.reference(path)
    return ref.get()


def add_meeting_to_database(the_data:object, meeting_id:str):
    ref = db.reference(f"/Meetings/{meeting_id}")
    ref.set(the_data)


def add_workshop_requests_to_database(the_data:object, workshop_id:str):
    ref = db.reference(f"/Workshop Requests/{workshop_id}")
    ref.set(the_data)


def validate_not_empty(ctx, param, value):
    if not value:
        raise click.BadParameter("Input cannot be empty")
    return value


def list_mentors(mentors:list):
    """Ensures that there are mentors to begin with. If not an error message is displayed."""
    try:
        for i in range(len(mentors)):
            if i == 0:
                click.secho("Available mentors:", fg="blue")

            key, mentor_data = mentors[i]

            if mentor_data.get("role") == "mentor":
                click.echo(f"\nMentor {i + 1}:")
                click.echo(f'Name: {mentor_data.get("full_name") or mentor_data.get("first_name")}')
                click.echo(f'Email: {mentor_data.get("email")}')
                click.echo(f'Expertise: {mentor_data.get("expertise")}')
    except Exception as e:
        click.secho(f"{e}: Unfortunately, there are no mentors available...", fg="gold", bg="white", blink=True)



def list_workshops():
    data = read_from_database("/Workshops Requests")
    i = 0

    try:
        # If user is indeed signed in. List all upcoming workshops
        for k,v in data.items():
            if i == 0:
                click.secho(f"\nUpcoming workshops:\n", fg="blue")

            click.echo(f"Topic {i + 1} - {v['topic']}")
            i += 1
    except Exception as e:
        click.secho(f"{e}: You have no upcoming workshops...", fg="gold", bg="white", blink=True)


def request_workshop(topic:str, id:str, date_requested:str):
    """This function will create a workshop request instance.

    It will also generate a unique random workshop id.
    """
    the_data = {
        "requestor_id": id,
        "topic": topic,
        "date_requested": date_requested
    }

    characters = string.ascii_letters + string.digits
    workshop_id = "".join(random.choice(characters) for _ in range(28))

    add_workshop_requests_to_database(the_data, workshop_id)
