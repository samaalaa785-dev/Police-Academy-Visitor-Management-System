# Smart Gate Entrance Visitor Management System

## 📌 Description
A Desktop + Web hybrid application to manage visitors using a **local network** for the Police Academy.  
The system allows visitor registration via a web form and internal staff management via a desktop GUI.  
It stores all submissions in a local SQLite database and supports exporting data to Excel for reporting.

---

## 🛠 Features
- 🖥 **Desktop GUI (PyQt6)** for staff to view/manage visitors
- 🌐 **Local Web Form (Flask)** for visitors to register their data
- 🔑 **QR Code generator** for quick visitor access to the form
- 🗄 **SQLite database** for offline storage
- 📊 **Export to Excel** for reporting and data analysis
- 🔍 **Search functionality** for internal staff records
- 🔒 **Field validation** (Name, National ID, Phone)
- 🕌 **Arabic-friendly UI** (RTL support)

---

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/Police-Academy-Visitor-Management-System.git
   cd Police-Academy-Visitor-Management-System
---
## ▶️ Usage

1.Run the application:

python main.py

2.Visitor Side:

-Connect to the local Wi-Fi / hotspot.

-Scan the generated QR Code.

-Fill out the visitor registration form.

-Submit your data (saved locally).

3.Staff Side:

-Use the desktop GUI to view visitors.

-Search/filter records.

-Export submissions to Excel.

---
## 📂 Project Structure

app/      # Flask backend + database

│── __init__.py

│── database.py

│── routes.py

│── templates/

│    ├── visit.html

│    └── thank_you.html

gui/                # PyQt6 desktop GUI

│── __init__.py

│── main_window.py

main.py             # Entry point

requirements.txt    # Dependencies

README.md           # Documentation

.gitignore          # Ignored files

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📜 License

This project is licensed under the encryptcore License.
You are free to use, modify, and distribute it with attribution.
