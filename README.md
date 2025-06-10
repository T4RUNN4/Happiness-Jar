# Happiness Jar
#### Description:

**Happiness Jar** is a digital adaptation of the well-known "Happiness Jar" concept. Inspired by the challenges of keeping physical jars in a small, shared workspace, this project was born out of a desire to create a private, secure, and mess-free version of the idea. Built using Flask, SQLite, HTML, CSS, JavaScript, and Bootstrap, this web app allows users to register, log in, and interact with their own virtual happiness jar.

Once logged in, users are welcomed with a clean, minimal interface featuring two main actions: "Adding a new happy memory" and "Retrieving a past one. If no memory is available, the site kindly reminds users to add some using contextual flash messages.

Key features include:
- **User Authentication**: Users can register and log in, with all input validated server-side for security.
- **Memory Management**: Users can add and retrieve happy memories, each associated with a mood and timestamp.
- **Mood Analytics**: A pie chart visualizes mood distribution, along with details like the happiest month and year.
- **Downloadable History**: Memories can be exported in CSV, TXT, or JSON formats.
- **User Experience**: Aesthetic choices like a soft background, rounded buttons, Poppins font, and cute illustrations create a soothing, joyful interface.
- **404 Handling**: Non-existent routes gracefully redirect to a custom 404 error page.
- **FAQ Page**: Includes context about the Happiness Jar concept for visitors who are not logged in.

---

### File Overview

```
happiness-jar/
├── app.py                 # Core Flask application
├── flask_session/         # Session storage directory
├── instance/
│   └── jar.db             # SQLite database (ignored via .gitignore)
├── requirements.txt       # Python package dependencies
├── static/
│   ├── faq.png            # Illustration for FAQ
│   ├── main.png           # Illustration for main page
│   ├── script.js          # JavaScript for frontend interactions
│   └── style.css          # Custom CSS styles
├── templates/
│   ├── 404.html           # Custom 404 page
│   ├── faq.html           # Explanation of the Happiness Jar
│   ├── history.html       # Page to view/download memory history
│   ├── index.html         # Dashboard after login
│   ├── layout.html        # Shared layout template
│   ├── login.html         # User login form
│   ├── mood.html          # Mood analysis page
│   ├── new.html           # Form to add a new memory
│   ├── past.html          # Page to view a past memory
│   └── register.html      # User registration form
├── .gitignore             # Files and folders to ignore in version control
├── .env                   # Environment variables (ignored in Git)
└── README.md              # This file
```

---

### Technologies Used

- **Flask** (with Jinja templating)
- **SQLite3**
- **Bootstrap 5**
- **Chart.js** (for mood data visualization)
- **CS50 Library for SQL**
- **Python-Dotenv** for environment management

CSS styling uses Bootstrap combined with custom design for a cute, uplifting theme. Animations are handled using Animate.css, while interactivity is powered by both Bootstrap JS and vanilla JavaScript.

External assets include:
```html
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

---

### Design Decisions

Creating this web version solved the real-life issues I had with physical jars: lack of space, privacy concerns, and risk of physical mess. Digitally, I could add helpful features like mood analytics and downloadable history — things not possible with paper notes.

Choosing SQLite was an intentional decision since it’s lightweight and sufficient for this small-scale app. Input validation, CSRF-safe forms, and secure password hashing (via `werkzeug.security`) were implemented to maintain data integrity and user safety.

While I initially aimed to deploy the app online (e.g., PythonAnywhere), I decided to postpone deployment due to complications with file structure and database handling in a hosted environment. However, all necessary components for deployment are in place, including a `.env` file, and I plan to revisit deployment soon.

---

### Final Notes

This is my final project submission for **CS50x**. I hope it inspires others to find joy in small moments — and to keep them safe, digitally. Some features are borrowed from Week 9 Finance to save some keystroke.
The website is a demo of the live project, so please don't register in that using your real credential because anyone can access them from the db file. Also, if you notice that the website is offline, please let me know that.
