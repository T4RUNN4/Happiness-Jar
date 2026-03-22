# Happiness Jar
![Homepage](/static/thumbnail.jpg)
#### Description:

**Happiness Jar** is a digital adaptation of the well-known "Happiness Jar" concept. Inspired by the challenges of keeping physical jars in a small, shared workspace, this project was born out of a desire to create a private, secure, and mess-free version of the idea. Built using Flask, SQLite, HTML, CSS, JavaScript, and Bootstrap, this web app allows users to register, log in, and interact with their own virtual happiness jar.

Once logged in, users are welcomed with a clean, minimal interface featuring two main actions: "Adding a new happy memory" and "Retrieving a past one. If no memory is available, the site kindly reminds users to add some using contextual flash messages.

Key features include:
- **User Authentication**: Users can register and log in, with all input validated server-side for security.
- **Memory Management**: Users can add and retrieve happy memories, each associated with a mood and timestamp.
- **Mood Analytics**: A pie chart visualizes mood distribution, along with details like the happiest month and year.
- **Downloadable History**: Memories can be exported in CSV, TXT, or JSON formats.
---

### Technologies Used

- **Flask** (with Jinja templating)
- **SQLite3**
- **Bootstrap 5**
- **Chart.js** (for mood data visualization)
- **CS50 Library for SQL**
- **Python-Dotenv** for environment management
- **ChartJS** for Charts

---

### Final Notes

This is my final project submission for **CS50x**. I hope it inspires others to find joy in small moments — and to keep them safe, digitally. Some features are borrowed from Week 9 Finance to save some keystrokes.
The website is a demo of the live project, so please don't register in that using your real credential because anyone can access them from the db file. Also, if you notice that the website is offline, please let me know that.
