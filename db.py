import mysql.connector
from mysql.connector import Error, IntegrityError
import hashlib



def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='todo_list',
            user='arnav',
            password='1234'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# Function to create tasks and users tables
def create_table():
    connection = create_connection()
    cursor = connection.cursor()

    # Create tasks table
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(255) NOT NULL,
        description VARCHAR(255),
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed BOOLEAN DEFAULT FALSE,
        user_id INT
    )
    """)

    # Create users table
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """)

    connection.commit()
    cursor.close()
    connection.close()


# Function to register a user
def register_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Encrypting password

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        connection.commit()
        cursor.close()
        connection.close()
        return True, "Registration successful!"
    except IntegrityError:
        cursor.close()
        connection.close()
        return False, "Username already taken. Please choose a different one."


# Function to log in a user
def login_user(username, password):
    connection = create_connection()
    cursor = connection.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Encrypting password

    cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, hashed_password))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user and isinstance(user[0], int):  # Check if user_id is an integer
        return user[0]  # Return user_id
    else:
        return None  # Invalid credentials


def complete_task(task_id):
    connection = create_connection()
    cursor = connection.cursor()

    # Update the task's status to complete (assuming you have a boolean or integer status column)
    query = "UPDATE tasks SET status = 1 WHERE id = %s"  # 1 indicates completed
    cursor.execute(query, (task_id,))

    connection.commit()
    cursor.close()
    connection.close()

# Function to add a task
def add_task(user_id, task_name, task_description):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO tasks (user_id, task, description) VALUES (%s, %s, %s)",
                   (user_id, task_name, task_description))
    connection.commit()
    cursor.close()
    connection.close()


# Function to retrieve tasks for a specific user
def get_tasks_by_user(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s ORDER BY date_added", (user_id,))
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    return tasks


# Function to delete a task by task_id
def delete_task(task_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    connection.commit()
    cursor.close()
    connection.close()


# Function to mark a task as completed
def complete_task(task_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET completed = TRUE WHERE id = %s", (task_id,))
    connection.commit()
    cursor.close()
    connection.close()


# Function to reset all tasks for a user
def reset_tasks(user_id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE user_id = %s", (user_id,))
    connection.commit()
    cursor.close()
    connection.close()
