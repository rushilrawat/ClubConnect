# ClubConnect 🚀

**Modern Club Management System for Student Clubs, Schools, and Colleges**

---

## 📖 About the Project

ClubConnect is a fully-featured, professional-grade Club Management System designed to simplify how schools, colleges, and student communities manage their members, awards, and activities.  

Built with a modern UI, real dashboards, smooth navigation, and powerful features — ClubConnect is your complete solution for managing all club-related operations. 🎓

---

## ✨ Features

- 🔐 **Login System** with Username/Password authentication and Dark Mode toggle
- 📊 **Modern Dashboard** with:
  - Total Members
  - Total Awards
  - Top Performer
  - Awards Category Pie Chart
  - Top Competitions Bar Chart
  - Awards Growth Line Chart (Over Years)
  - Class-wise Students Pie Chart
- 👥 **Manage Members**
  - Add, View, Search, Delete, Export Members to Excel
- 🏆 **Manage Awards**
  - Add, View, Search, Delete, Export Awards to Excel
- 💾 **Backup Database** (Create a full database backup with one click)
- 🌗 **Dark and Light Theme Switching** everywhere
- 📄 **Export to Excel** easily (Members and Awards Data)
- 📈 **Growth Charts and Visual Analytics**
- 🛠️ **Settings Panel** for future features (Theme toggle, Username display)
- 🎨 **Clean Responsive UI** (3-Panel Layout: Left - Center - Right)

---

## 🛠️ Technologies Used

- **Python 3.11+**
- **Tkinter** (Frontend GUI)
- **Matplotlib** (Charts and Visualizations)
- **Pandas** (Excel Export Handling)
- **OpenPyXL** (Excel file creation and management)
- **SQLite3** (Lightweight Embedded Database)

---

## 📥 Installation Guide

1. **Clone the Repository**
```
git clone https://github.com/rushilrawat/ClubConnect.git
cd ClubConnect
```
2. **Install Required Packages**
```
pip install pandas openpyxl matplotlib
```
3. **Run the Application**
```
python main.py
```
✅ Done! You can now login and manage your ClubConnect system easily!
---
```
ClubConnect/
├── database/
│   ├── db_helper.py
│   ├── clubconnect.db
│   ├── users.db
│
├── ui/
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── member_management.py
│   ├── award_management.py
│   ├── settings_page.py
│
├── utils/
│   ├── theme_manager.py
│   ├── ui_helpers.py
│
├── assets/
│   └── logos/
│       └── clubconnect_logo.png
│
├── backups/
│   └── (auto-created backups)
│
├── main.py
├── README.md
├── requirements.txt
```
---

## 🚀 Future Improvements

1. 📨 Email Notifications for Awards and Membership Changes
2. 🌐 Full Web App version (using Django or Flask)
3. 📋 Member Profile Pages
4. 🔔 In-App Notifications System
5. 🎯 Role-based Access Control (Admin vs Member)
6. 🔄 Live Sync with Google Sheets or Cloud Database
---

## 📜 License
This project is licensed under MIT License - Feel free to use and contribute!

---
## 📢 Version History
1. Project started in January, 2023.
2. Version 2 out in Feb, 2024.
3. Version 3 expected release: May, 2025

---

## 🙌 Acknowledgements
Developed with ❤️ by Rushil Rawat.

Thanks for using and improving ClubConnect!

