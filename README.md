# SkillSync CLI

**SkillSync** is a Python-based Command-Line Interface (CLI) application for managing workshop bookings and one-on-one mentorship or peer meetings. Built entirely for terminal use, the app uses Firebase for authentication and database management, and the Google Calendar API for scheduling meetings. It enforces strict booking rules: weekdays only, from 07:00 to 17:00.

The app is packaged for distribution using PyInstaller and designed with a smooth and interactive CLI experience using the `click` library.

---

## 🚀 Features

### 🔐 Authentication
- Secure sign-up and login using Firebase Authentication (REST API).
- Role-based user access (mentor or peer).
- User details stored in Firestore.

### 📅 Booking System
- **Mentor Sessions**: List and request meetings with available mentors.
- **Peer Sessions**: Find peers based on availability or expertise and book sessions.

### 🗓 Google Calendar Integration
- Creates calendar events automatically for confirmed bookings.
- Sends calendar invites to all participants.
- Enforces all meetings to occur on **weekdays only**, **07:00 to 17:00**.

### 💻 CLI Interface
SkillSync is built using the `click` library, offering the following terminal commands:

- `Login` – Authenticate and log in the user
- `View Workshops` – View a list of workshops and mentors
- `Request Workshop` – Request mentors to cover a specific topic
- `Request Meeting` – Book a session with a mentor or peer
- `View Bookings` – Show all confirmed bookings
- `Cancel Booking` – Cancel an existing session
- `Sign Out` – Terminate session and log out

---

## ⚙️ Technical Stack

- **Python 3.10+**
- **Firebase Admin SDK** – For authentication and Firestore database
- **Google Calendar API** – For event creation and scheduling
- **Click** – For building the command-line interface
- **PyInstaller** – For packaging the app as a standalone executable

---

## 📌 Time Constraints

All meetings are restricted to:
- **Weekdays (Monday to Friday)**
- **Between 07:00 and 17:00**

This constraint is enforced both in the app logic and within Google Calendar integration.

---

## 🌟 Stretch Features (1/3 implemented)

- ✅ **Email Notifications**: Meeting confirmations and reminders using `smtplib`
- ✅ **Feedback System**: Users can rate and leave reviews for sessions
- ✅ **Search Filters**: Filter mentors or peers by expertise or availability

---

## 💾 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/skillsync.git
cd skillsync
```

### 2. Create a Virtual Environment (optional)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Required Packages
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file or set the following environment variables:

```env
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/firebase-service-account.json
FIREBASE_API_KEY=your_firebase_web_api_key
```

### 5. Run the Application
```bash
python main.py --help
```

---

## 📦 Packaging for Distribution

To create a standalone executable file:

```bash
pyinstaller --onefile main.py
```

The executable will be found in the `dist/` folder.

---

## ✅ Completed Milestones

- Firebase Authentication and Firestore setup
- Full CLI workflow with `click`
- Google Calendar integration with invite sending
- Role-based booking system
- Time-restricted scheduling
- Packaged with PyInstaller

---

## 👨‍💻 Author

**Bill Qubeka**  
📧 billqubeka@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/bill-qubeka/)  
🔗 [GitHub](https://github.com/billandro)

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

---
