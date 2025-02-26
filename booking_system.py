from firebase_admin import auth, db
from firebase_admin import credentials
from main import connect_to_database
from shared import read_from_database
import click
import datetime
import calender


@click.group()
def cli_2():
    """This is the grouper of all the commands"""
    pass


@cli_2.command()
def mentor_list():
    """Display available mentors"""
    connect_to_database()

    mentor_list = []
    users = read_from_database("/Users")

    for key, value in users.items():
        if value["role"] == "mentor":
            mentor_list.append([key, value])

    for i in range(len(mentor_list)):
        if i == 0:
            click.echo("List of available mentors....")
        click.echo(f"\nMentor {i + 1}:")
        click.echo(f"Name: {mentor_list[i][1]['first_name']}")
        click.echo(f"Email address: {mentor_list[i][1]['email']}")
        click.echo(f"Expertise: {mentor_list[i][1]['expertise']}")

    return mentor_list


def validate_not_empty(ctx, param, value):
    if not value:
        raise click.BadParameter("Input cannot be empty")
    return value


def time_restrictions(day):
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday"]

    while day not in weekdays:
        day = input("Please choose a day:")


@cli_2.command()
def choose_mentor(email):
    """Book mentor/mentors for session"""
    # meeting_id: {mentor_id, mentee_id, time, status}
    mentors = mentor_list()
    done = False
    chosen_mentors = []
    user = auth.get_user_by_email(email)
    # booking_datetime = datetime.strptime(time, "%Y-%m-%d %H:%M")
    booking_time = "2025-02-26 10:30"

    while not done:
        chosen_mentor = click.option(prompt="Enter the mentor you would like to book by name (e.g. 'Bill')", value_proc=validate_not_empty).strip().lower()
        try:
            for i in range(len(mentors)):
                for key, value in mentors[i][1].items(): 
                    if chosen_mentor == value["first_name"]:
                        chosen_mentors.append(key)

                        meeting_id = {"mentor_id": key, "mentee_id": user.uid, "time": booking_time, "status": "active"}
                        break
                break
        except:
            click.secho(f"Chosen mentor, '{chosen_mentor}', is not in our system.", fg="red")
        finally:
            select_again = click.confirm("Would you like to book another mentor?")

            if select_again == "y":
                done = False
                continue
            else:
                click.echo("Booking completed successfully...")
                done = True

    click.echo(f"Chosen mentors: {chosen_mentors}")