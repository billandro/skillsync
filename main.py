import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import auth
import json

# Class to create a user instance
class User:
    def __init__(self, name, email, role, password):
        self.name = name
        self.email = email
        self.role = role
        self.role = password

    def change_name(self, new_name):
        self.name = new_name

    def __str__(self):
        return f"{self.name}, {self.email}, {self.role}"


def connect_to_database():
    cred = credentials.Certificate("skillsync-project-451208-firebase-adminsdk-fbsvc-247be52390.json")
    firebase_admin.admin(cred, {
        "databaseURL": "https://skillsync-project-451208-default-rtdb.firebaseio.com/"
    })


def read_from_database(path):
    ref = db.reference(path)
    snapshot = ref.get()


def write_to_the_database(path):
    ref = db.reference(path)
    ref.set({
    })

    
def update_data():
    ref = db.reference('your_data_path')
    ref.update({
        'age': 31
    })

def authentic_user(name:str, email:str, password:int):
    # name, email, role, password
    user = auth.create_user(
        display_name = name,
        email = email,
        password = password,
    )

    print(f"user ID: {user.uid}, password: {user.password}, name: {user.display_name}, email: {user.email}")
    
    # Prompt the user for a role
    role = input("Are you signing up to be a MENOTOR or PEER?: ").strip()
    user.uid = User(user.name, user.email, user.role, user.password)
    
    ref = db.reference(f"/Users/{user.uid}")
    user_details = {
        "name": user.name,
        "email": user.email,
        "role": role,
        "password": user.password,
    }
    file_contents = json.load(user_details)
    print(file_contents)
    # ref.set()

print(authentic_user("example", "example.gmail.com", 0000))
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


def main():
    # Connect to the databade first
    connect_to_database()

    #
    