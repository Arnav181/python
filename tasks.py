from db import add_task, get_tasks_by_user, delete_task, complete_task, register_user, login_user

class TaskManager:
    @staticmethod
    def register_user(username, password):
        return register_user(username, password)

    @staticmethod
    def login_user(username, password):
        return login_user(username, password)

    @staticmethod
    def add_new_task(task, description, user_id):
        add_task(task, description, user_id)

    @staticmethod
    def retrieve_tasks(user_id):
        return get_tasks_by_user(user_id)

    @staticmethod
    def remove_task(task_id):
        delete_task(task_id)

    @staticmethod
    def mark_task_completed(task_id):
        complete_task(task_id)
