from firebase_admin import auth, db
from firebase_admin import credentials
from main import connect_to_database
from shared import read_from_database

def mentor_list():
    """Display available mentors"""
    connect_to_database()

    mentor_list = []
    users = read_from_database("/Users")

    for key, value in users.items():
        if value["role"] == "mentor":
            mentor_list.append(value)

    for i in range(len(mentor_list)):
        if i == 0:
            print("List of available mentors....")
        print(f"\nMentor {i + 1}:")
        print(f"Name: {mentor_list[i]['first_name']}")
        print(f"Email address: {mentor_list[i]['email']}")
        print(f"Expertise: {mentor_list[i]['expertise']}")


def choose_mentor():
    """Book mentor/mentors for session"""
    # meeting_id: {mentor_id, mentee_id/peer_id, time, status}


mentor_list()