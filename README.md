# 🎓 Learning-365 | Next-Gen Learning Management System (LMS)

![Project Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0%2B-092E20?style=for-the-badge&logo=django&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

> **Learning-365** is a futuristic, AI-powered Learning Management System designed to bridge the gap between students and modern education. Featuring a **Cyberpunk/Glassmorphism UI**, it offers secure AI exams, live class integration, and a rich digital library.

---

## 📸 Project Glimpse

| Student Dashboard | AI Exam Portal |
| :---: | :---: |
| ![Dashboard](https://via.placeholder.com/600x300/111/00d4ff?text=Dashboard+UI) | ![Exam](https://via.placeholder.com/600x300/111/ff3366?text=Secure+Exam+UI) |

---

## 🚀 Key Features

### 👨‍🎓 **Student Panel**
* **Interactive Dashboard:** Personalized welcome screen with course progress tracking.
* **Modern UI:** Dark theme featuring Neon Glow effects and Glassmorphism design.
* **Smart Notifications:** Real-time updates for exams and classes.

### 📝 **AI Assessment Center (Secure Exams)**
* **Anti-Cheat System:** Full-screen enforcement and tab-switch detection.
* **Auto-Grading:** Instant result generation upon submission.
* **Timer Based:** Strict countdown timers for assessments.
* **Result History:** Detailed performance analytics.

### 🎥 **Live Classes & Library**
* **Live Schedule:** Integration with Zoom/Google Meet for real-time classes.
* **Digital Archive:** Downloadable lecture notes, assignments, and PDFs.
* **Search & Filter:** Advanced search functionality for resources.

### 🔒 **Security & Profile**
* **Secure Auth:** Login/Register system with encrypted passwords.
* **Profile Management:** Custom avatar upload with camera UI.

---

## 🛠️ Tech Stack

* **Backend:** Django (Python Framework)
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
* **Styling:** Custom Glassmorphism CSS, FontAwesome Icons
* **Database:** SQLite (Default) / PostgreSQL (Production ready)

---

## ⚙️ Installation & Setup Guide

Follow these steps to set up the project locally on your machine.

### **Prerequisites**
Make sure you have the following installed:
* [Python 3.10+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)

### **Step 1: Clone the Repository**
Open your terminal/command prompt and run:
```bash
git clone [https://github.com/Anubhav2321/collage-management-.git](https://github.com/Anubhav2321/collage-management-.git)
cd collage-management-
```
### Step 2: Create & Activate Virtual Environment
It is highly recommended to isolate package dependencies.

For Windows:
PowerShell
```
python -m venv .venv
.venv\Scripts\activate
```
(You will see (.venv) at the start of your terminal line once activated.)

### Step 3: Install Dependencies
Install all required libraries/packages from the requirements file:
Bash
```
pip install -r requirements.txt
```
### Step 4: Configure Environment Variables
Create a file named .env in the root directory (where manage.py is located) and add the following configuration:

Code snippet
```DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here
```

# Add any other API keys here if needed

### Step 5: Database Setup
Apply migrations to create the database schema:

Bash
```
python manage.py makemigrations
python manage.py migrate
```
### Step 6: Create Admin User
Create a superuser to access the Django admin panel:

Bash
```
python manage.py createsuperuser
```
(Follow the prompts to set a username, email, and password.)

### Step 7: Run the Server
Start the local development server:

Bash
```
python manage.py runserver
```

### 📂 Project Structure
Here is an overview of the file structure for the project:
```
Learning-365/
│
├── .venv/                # Virtual Environment (Ignored in Git)
├── media/                # User uploaded files (Images/PDFs) (Ignored in Git)
├── static/               # CSS, JS, Images (Assets)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/            # HTML Files
│   ├── base.html
│   ├── dashboard.html
│   └── ...
├── your_app_name/        # Main Application Logic
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── manage.py             # Django Entry Point
├── requirements.txt      # List of dependencies
├── .env                  # Environment Variables (Ignored in Git)
└── README.md             # Project Documentation
```
📞 Contact & Support
If you have any questions, feedback, or need support running this project, feel free to reach out:

Developer: 
Anubhav Samanta

GitHub: 
```
https://github.com/Anubhav2321?tab=repositories
```
Email: anubhavsamanta2005@gmail.com

          
