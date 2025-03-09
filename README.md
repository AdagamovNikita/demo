# Flask Todo App

A simple todo application built with Flask and SQLite.

## Features

- Add new tasks
- Mark tasks as completed/uncompleted
- Delete tasks
- Search tasks
- Responsive design with Bootstrap

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd hello_flask
```

2. Install the required packages:
```bash
pip install flask
```

3. Initialize the database:
```bash
python init_db.py
```

4. Run the application:
```bash
python app.py
```

5. Open http://127.0.0.1:5000 in your web browser

## Project Structure

```
hello_flask/
│── app.py              # Main Flask application
│── init_db.py          # Database initialization script
│── templates/          # HTML templates
│   ├── index.html      # Home page
│   ├── tasks.html      # Tasks page
│── static/             # Static files (CSS, JS, images)
```

## Requirements

- Python 3.x
- Flask
- SQLite3 