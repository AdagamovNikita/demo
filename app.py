import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    search_query = request.form.get('search')
    if search_query:
        cursor.execute('SELECT * FROM tasks WHERE title LIKE ? ORDER BY completed', (f'%{search_query}%',))
    else:
        search_query = ""
        cursor.execute('SELECT * FROM tasks ORDER BY completed')

    tasks = cursor.fetchall()
    conn.close()
    return render_template('tasks.html', tasks=tasks, search_query=search_query)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    conn.commit()
    conn.close()
    return redirect(url_for('tasks'))

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle(id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT completed FROM tasks WHERE id = ?', (id,))
    current_status = cursor.fetchone()[0]
    
    # Проверяем текущий статус задачи
    if current_status == 0:
        # Если задача не выполнена (0), меняем статус на выполнено (1)
        new_status = 1
    else:
        # Если задача выполнена (1), меняем статус на не выполнено (0)
        new_status = 0
    
    cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (new_status, id))
    conn.commit()
    conn.close()
    return redirect(url_for('tasks'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True) 