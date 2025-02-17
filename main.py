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

tumiso = User("Tumiso", "example@gmail.com", "Software Engineer")
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

    # with open("example.json", "r") as f:
    #     file_contents = json.load(f)
    # ref.set(file_contents)

    
def update_data():
    ref = db.reference('your_data_path')
    ref.update({
        'age': 31
    })


user = auth.create_user(
    email='user@example.com',
    password='password',
    display_name='John Doe',
    photo_url='https://example.com/photo.jpg'
)
print(user.uid)

# ref = db.reference("/Books/Best_Sellers/")
# best_sellers = ref.get()
# print(best_sellers)
# for key, value in best_sellers.items():
#     if(value["Author"] == "J.R.R. Tolkien"):
#         value["Price"] = 90
#         ref.child(key).update({"Price":80})