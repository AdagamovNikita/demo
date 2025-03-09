import sqlite3  # Импортируем модуль для работы с базой данных SQLite
from flask import Flask, render_template, request, redirect, url_for  # Импортируем необходимые функции и классы из Flask

app = Flask(__name__)  # Создаем экземпляр приложения Flask

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')  # Рендерим шаблон index.html для отображения главной страницы

# Маршрут для отображения списка задач и поиска (поддерживает методы GET и POST)
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    conn = None  # Инициализируем переменную для соединения с базой данных (на данный момент ещё нет подключения)
    tasks = []   # Инициализируем пустой список для хранения задач
    search_query = request.form.get('search')  # Получаем поисковый запрос из формы (если он был отправлен)
    
    try:
        # Пытаемся установить соединение с базой данных 'todo.db'
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()  # Создаем курсор для выполнения SQL-запросов

        if search_query:
            # Если есть поисковый запрос, выбираем задачи, где название содержит искомую подстроку
            cursor.execute(
                'SELECT * FROM tasks WHERE title LIKE ? ORDER BY completed', 
                (f'%{search_query}%',)
            )
        else:
            search_query = ""  # Если поискового запроса нет, устанавливаем пустую строку
            # Выбираем все задачи, сортируя их по статусу выполнения (completed)
            cursor.execute('SELECT * FROM tasks ORDER BY completed')

        tasks = cursor.fetchall()  # Получаем все строки (задачи) из результата запроса
    except Exception as e:
        # Если возникает ошибка при работе с базой данных, выводим сообщение об ошибке
        print("Ошибка при выполнении запроса к базе данных:", e)
    finally:
        if conn:
            # Независимо от результата, закрываем соединение с базой данных, если оно было установлено
            conn.close()
    # Передаем список задач и поисковый запрос в шаблон tasks.html для отображения
    return render_template('tasks.html', tasks=tasks, search_query=search_query)

# Маршрут для добавления новой задачи (метод POST)
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']  # Получаем значение названия новой задачи из данных формы
    conn = None  # Инициализируем переменную для соединения с базой данных
    try:
        # Пытаемся установить соединение с базой данных 'todo.db'
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()  # Создаем курсор для выполнения SQL-запросов
        # Выполняем запрос для вставки новой задачи в таблицу tasks, передавая название задачи
        cursor.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
        conn.commit()  # Фиксируем изменения в базе данных
    except Exception as e:
        # Если возникает ошибка при добавлении задачи, выводим сообщение об ошибке
        print("Ошибка при добавлении задачи:", e)
    finally:
        if conn:
            # Закрываем соединение с базой данных, если оно было успешно установлено
            conn.close()
    # Перенаправляем пользователя на страницу со списком задач после добавления новой записи
    return redirect(url_for('tasks'))

# Маршрут для переключения статуса выполнения задачи (отметить как выполненную/не выполненную)
@app.route('/toggle/<int:id>', methods=['POST'])
def toggle(id):
    conn = None  # Инициализируем переменную для соединения с базой данных
    try:
        # Подключаемся к базе данных 'todo.db'
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()  # Создаем курсор для выполнения SQL-запросов
        # Выполняем запрос для получения текущего статуса задачи по её ID
        cursor.execute('SELECT completed FROM tasks WHERE id = ?', (id,))
        row = cursor.fetchone()  # Получаем первую строку результата запроса
        if row is not None:
            current_status = row[0]  # Извлекаем текущий статус задачи (0 - не выполнена, 1 - выполнена)
            # Меняем статус задачи более подробно:
            if current_status == 0:
                new_status = 1  # Если задача не выполнена, устанавливаем статус "выполнена"
            else:
                new_status = 0  # Если задача выполнена, устанавливаем статус "не выполнена"
            # Выполняем обновление статуса задачи в базе данных
            cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (new_status, id))
            conn.commit()  # Фиксируем изменения
        else:
            # Если задача с указанным ID не найдена, выводим сообщение об этом
            print("Задача с указанным ID не найдена")
    except Exception as e:
        # Если возникает ошибка при переключении статуса задачи, выводим сообщение об ошибке
        print("Ошибка при переключении статуса задачи:", e)
    finally:
        if conn:
            # Независимо от результата, закрываем соединение с базой данных, если оно было установлено
            conn.close()
    # Перенаправляем пользователя обратно на страницу со списком задач
    return redirect(url_for('tasks'))

# Маршрут для удаления задачи по её ID
@app.route('/delete/<int:id>')
def delete(id):
    conn = None  # Инициализируем переменную для соединения с базой данных
    try:
        # Подключаемся к базе данных 'todo.db'
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()  # Создаем курсор для выполнения SQL-запросов
        # Выполняем запрос для удаления задачи с заданным ID из таблицы tasks
        cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
        conn.commit()  # Фиксируем изменения в базе данных
    except Exception as e:
        # Если возникает ошибка при удалении задачи, выводим сообщение об ошибке
        print("Ошибка при удалении задачи:", e)
    finally:
        if conn:
            # Гарантированно закрываем соединение с базой данных, если оно было установлено
            conn.close()
    # Перенаправляем пользователя обратно на страницу со списком задач после удаления
    return redirect(url_for('tasks'))

# Запуск приложения, если этот скрипт запущен напрямую
if __name__ == '__main__':
    app.run(debug=True)  # Запускаем сервер Flask в режиме отладки, что позволяет видеть подробные сообщения об ошибках
