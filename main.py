import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import auth
import json


# def read_from_database(path):
#     ref = db.reference(path)
#     snapshot = ref.get()

# def write_to_the_database(path):
#     ref = db.reference(path)
#     ref.set({
#     })

# def update_data():
#     ref = db.reference('your_data_path')
#     ref.update({
#         'age': 31
#     })


def connect_to_database():
    cred = credentials.Certificate("skillsync-project-451208-firebase-adminsdk-fbsvc-247be52390.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://skillsync-project-451208-default-rtdb.firebaseio.com/"
    })


def login():
    print("Log in...")
    email = input("Enter email: ")
    password = input("Enter password: ")
    guy = auth.get_user_by_email(email)
    print(type(guy))
    print(guy)
    

def sign_up():
    print("Sign up.....")
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()
    first_name = input("Enter first name: ").strip()
     
    # Prompt the user for a role
    role = input("Are you signing up to be a 'MENTOR' or 'PEER'?: ").strip().lower()
    expertise = input("What is your expertise?: ").strip().lower()

    try:
        authenticate_user(first_name, email, role, password, expertise)
    except auth.EmailAlreadyExistsError:
        print("Error: email already exists")


def authenticate_user(full_name:str, email:str, role:str, password:int, expertise:str):
    user = auth.create_user(
        display_name = full_name,
        email = email,
        password = password,
    )
    print(f"user_id: {user.uid}, full_name: {user.display_name}, email: {user.email}, role: {role}, expertise: {expertise}")
    
    # ref = db.reference(f"/Users/{user.uid}")
    the_id = user.uid
    the_user = {
        "full_name": full_name,
        "email": email,
        "role": role,
        "expertise": expertise,
    }

    print(f"{user.uid}")
    # file_contents = json.load(user.uid)
    # print(type(file_contents))


def main():
    # Connect to the databade first
    connect_to_database()
    returning_user = input("Are you a returning user?[y/n] ").strip().lower()

    if returning_user == "y":
        login()
    elif returning_user == "n":
        sign_up()


main()


# print(authentic_user("example", "example.gmail.com", 0000))
# ref = db.reference("/Books/Best_Sellers/")
# best_sellers = ref.get()
# print(best_sellers)
# for key, value in best_sellers.items():
#     if(value["Author"] == "J.R.R. Tolkien"):
#         value["Price"] = 90
#         ref.child(key).update({"Price":80})


# ref = db.reference("user")
#     snapshot = ref.get()

# with open("book_info.json", "r") as f:
#         file_contents = json.load(f)
#     ref.set(file_contents)
    
    