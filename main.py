import sys

from PyQt5 import QtGui
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QHBoxLayout, QListWidget, QLineEdit, QTextEdit,
                             QListWidgetItem, QLabel, QMessageBox)

for_text = "color: rgb(239, 240, 241);"
for_button = "color: rgb(239, 240, 241);"
for_line = "border: 1px solid rgb(50, 50, 50); background-color: rgb(30, 30, 30); color: rgb(239, 240, 241);"
font = QtGui.QFont()
font.setFamily("Bahnschrift SemiLight")
font.setPointSize(11)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.tasks_list = QListWidget(self)
        self.tasks_list.setStyleSheet(for_line)
        self.tasks_list.setFont(font)
        self.button_all_tasks = QPushButton("Все задачи", self)
        self.button_all_tasks.setStyleSheet(for_button)
        self.button_all_tasks.setFont(font)
        self.button_active_tasks = QPushButton("Активные задачи", self)
        self.button_active_tasks.setStyleSheet(for_button)
        self.button_active_tasks.setFont(font)
        self.button_done_tasks = QPushButton("Выполненные задачи", self)
        self.button_done_tasks.setStyleSheet(for_button)
        self.button_done_tasks.setFont(font)
        self.task_name = QLineEdit(self)
        self.task_name.setStyleSheet(for_line)
        self.task_name.setFont(font)
        self.task_description = QTextEdit(self)
        self.task_description.setStyleSheet(for_line)
        self.task_description.setFont(font)
        self.button_add_task = QPushButton("Добавить задачу", self)
        self.button_add_task.setStyleSheet(for_button)
        self.button_add_task.setFont(font)
        self.button_edit_task = QPushButton("Изменить задачу", self)
        self.button_edit_task.setStyleSheet(for_button)
        self.button_edit_task.setFont(font)
        self.button_delete_task = QPushButton("Удалить задачу", self)
        self.button_delete_task.setStyleSheet(for_button)
        self.button_delete_task.setFont(font)
        self.categories_list = QListWidget(self)
        self.categories_list.setStyleSheet(for_line)
        self.categories_list.setFont(font)
        self.category_name = QLineEdit(self)
        self.category_name.setStyleSheet(for_line)
        self.category_name.setFont(font)
        self.button_add_category = QPushButton("Добавить категорию", self)
        self.button_add_category.setStyleSheet(for_button)
        self.button_add_category.setFont(font)
        self.button_edit_category = QPushButton("Изменить категорию", self)
        self.button_edit_category.setStyleSheet(for_button)
        self.button_edit_category.setFont(font)
        self.button_delete_category = QPushButton("Удалить категорию", self)
        self.button_delete_category.setStyleSheet(for_button)
        self.button_delete_category.setFont(font)
        self.button_edit_status_false = QPushButton("Готово", self)
        self.button_edit_status_false.setStyleSheet(for_button)
        self.button_edit_status_false.setFont(font)
        self.button_edit_status_true = QPushButton('В процессе', self)
        self.button_edit_status_true.setStyleSheet(for_button)
        self.button_edit_status_true.setFont(font)

        self.tasks_list.itemClicked.connect(self.task_detail)
        self.categories_list.itemClicked.connect(self.category_detail)
        self.button_add_task.clicked.connect(self.add_task)
        self.button_delete_task.clicked.connect(self.delete_task)
        self.button_add_category.clicked.connect(self.add_category)
        self.button_delete_category.clicked.connect(self.delete_category)
        self.button_edit_task.clicked.connect(self.edit_task)
        self.button_edit_category.clicked.connect(self.edit_category)
        self.button_edit_status_false.clicked.connect(self.edit_status_false)
        self.button_edit_status_true.clicked.connect(self.edit_status_true)
        self.button_all_tasks.clicked.connect(self.load_tasks)
        self.button_active_tasks.clicked.connect(self.load_active_tasks)
        self.button_done_tasks.clicked.connect(self.load_done_tasks)

        self.init_ui()
        self.create_db()
        self.load_categories()
        self.load_active_tasks()

    def init_ui(self):
        self.resize(600, 700)
        self.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.setWindowTitle("Список задач")
        vbox = QVBoxLayout()
        self.name_label = 'Все задачи:'
        self.name1 = QLabel(self.name_label, self)
        self.name1.setStyleSheet(for_text)
        self.name1.setFont(font)
        vbox.addWidget(self.name1)
        vbox.addWidget(self.tasks_list)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_all_tasks)
        hbox.addWidget(self.button_active_tasks)
        hbox.addWidget(self.button_done_tasks)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_edit_status_false)
        hbox.addWidget(self.button_edit_status_true)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        self.name2 = QLabel('Название задачи:', self)
        self.name2.setStyleSheet(for_text)
        self.name2.setFont(font)
        hbox.addWidget(self.name2)
        hbox.addWidget(self.task_name)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        self.name3 = QLabel('Описание задачи:', self)
        self.name3.setStyleSheet(for_text)
        self.name3.setFont(font)
        hbox.addWidget(self.name3)
        hbox.addWidget(self.task_description)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        self.name4 = QLabel('Категория:', self)
        self.name4.setStyleSheet(for_text)
        self.name4.setFont(font)
        hbox.addWidget(self.name4)
        hbox.addWidget(self.category_name)
        vbox.addLayout(hbox)
        self.name5 = QLabel('Список категорий:', self)
        vbox.addWidget(self.name5)
        self.name5.setStyleSheet(for_text)
        self.name5.setFont(font)
        vbox.addWidget(self.categories_list)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_add_task)
        hbox.addWidget(self.button_edit_task)
        hbox.addWidget(self.button_delete_task)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_add_category)
        hbox.addWidget(self.button_edit_category)
        hbox.addWidget(self.button_delete_category)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def create_db(self):
        query = QSqlQuery()

        query.exec(
            """
            CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL
            );
            """
        )
        query.exec(
            """
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            active BOOL NOT NULL DEFAULT TRUE,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (id)
            );
            """
        )

    def load_categories(self):
        query = QSqlQuery()
        query.exec(
            """SELECT * 
            FROM categories;""")
        self.categories = []
        count = query.record().count()
        while query.next():
            temp = []
            for i in range(count):
                temp.append(query.value(i))
            self.categories.append(temp)
        print(self.categories)
        self.categories_list.clear()
        for category in self.categories:
            self.categories_list.addItem(QListWidgetItem(category[1]))

    def load_tasks(self):
        query = QSqlQuery()
        query.exec(
            """SELECT * 
            FROM tasks
            LEFT JOIN categories 
            ON category_id=categories.id;""")
        self.tasks = []
        count = query.record().count()
        while query.next():
            temp = []
            for i in range(count):
                temp.append(query.value(i))
            self.tasks.append(temp)
        print(self.tasks)
        self.tasks_list.clear()
        for task in self.tasks:
            self.tasks_list.addItem(QListWidgetItem(task[1]))
        self.name1.setText("Все задачи: ")

    def load_active_tasks(self):
        query = QSqlQuery()
        query.exec(
            """SELECT * 
            FROM tasks
            LEFT JOIN categories
            ON category_id=categories.id
            WHERE active = TRUE;""")
        self.tasks = []
        count = query.record().count()
        while query.next():
            temp = []
            for i in range(count):
                temp.append(query.value(i))
            self.tasks.append(temp)
        print(self.tasks)
        self.tasks_list.clear()
        for task in self.tasks:
            self.tasks_list.addItem(QListWidgetItem(task[1]))
        self.name1.setText("Активные задачи: ")

    def load_done_tasks(self):
        query = QSqlQuery()
        query.exec(
            """SELECT * 
            FROM tasks
            LEFT JOIN categories
            ON category_id=categories.id
            WHERE active = FALSE;""")
        self.tasks = []
        count = query.record().count()
        while query.next():
            temp = []
            for i in range(count):
                temp.append(query.value(i))
            self.tasks.append(temp)
        print(self.tasks)
        self.tasks_list.clear()
        for task in self.tasks:
            self.tasks_list.addItem(QListWidgetItem(task[1]))
        self.name1.setText("Выполненные задачи: ")

    def add_task(self):
        name = self.task_name.text()
        description = self.task_description.toPlainText()
        row = self.categories_list.currentRow()
        print(name, description, row)
        category_id = self.categories[row][0]
        query = QSqlQuery()
        query.exec(
            f"""INSERT INTO tasks (name, description, category_id)
            VALUES ('{name}', '{description}', '{category_id}');"""
        )
        self.load_tasks()

    def add_category(self):
        name = self.category_name.text()
        query = QSqlQuery()
        query.exec(
            f"""INSERT INTO categories (name)
            VALUES ('{name}');"""
        )
        self.load_categories()

    def task_detail(self):
        print(self.tasks)
        row = self.tasks_list.currentRow()
        self.task_name.setText(self.tasks[row][1])
        self.task_description.setText(self.tasks[row][2])
        self.category_name.setText(self.tasks[row][6])

    def category_detail(self):
        row = self.categories_list.currentRow()
        print(self.categories[row][1])
        self.category_name.setText(self.categories[row][1])

    def delete_task(self):
        row = self.tasks_list.currentRow()
        task_id = self.tasks[row][0]
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText(f"Вы точно хотите удалить задачу: {self.tasks[row][1]}?")
        message_box.setWindowTitle("Удалить категорию?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.show()
        result = message_box.exec()
        if result == QMessageBox.Yes:
            query = QSqlQuery()
            query.exec(
                f"""DELETE FROM tasks 
                WHERE id={task_id};"""
            )
        self.load_tasks()

    def delete_category(self):
        row = self.categories_list.currentRow()
        category_id = self.categories[row][0]
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText(f"Вы точно хотите удалить категорию: {self.categories[row][1]}?")
        message_box.setWindowTitle("Удалить категорию?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.show()
        result = message_box.exec()
        if result == QMessageBox.Yes:
            query = QSqlQuery()
            query.exec(
                f"""DELETE FROM categories
                                   WHERE id={category_id};"""
            )
            self.load_categories()

    def edit_category(self):
        row = self.categories_list.currentRow()
        category_id = self.categories[row][0]
        name = self.category_name.text()
        query = QSqlQuery()
        query.exec(
            f'''UPDATE categories
            SET name = '{name}'
            WHERE id = {category_id};'''
        )
        self.load_categories()

    def edit_task(self):
        row = self.tasks_list.currentRow()
        task_id = self.tasks[row][0]
        name = self.task_name.text()
        description = self.task_description.toPlainText()
     #   cat_row = self.tasks_list.currentRow()
     #   category_id = self.categories[cat_row][0]
        query = QSqlQuery()
        query.exec(
            f'''UPDATE tasks
            SET name = '{name}', description = '{description}'
            WHERE id = {task_id};'''
        )
        self.load_tasks()

    def edit_status_false(self):
        row = self.tasks_list.currentRow()
        task_id = self.tasks[row][0]
        query = QSqlQuery()
        query.exec(
            f'''UPDATE tasks
            SET active = FALSE
            WHERE id = {task_id};'''
        )
        self.load_done_tasks()

    def edit_status_true(self):
        row = self.tasks_list.currentRow()
        task_id = self.tasks[row][0]
        query = QSqlQuery()
        query.exec(
            f'''UPDATE tasks
            SET active = TRUE
            WHERE id = {task_id};'''
        )
        self.load_active_tasks()

if __name__ == '__main__':
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("tasks_list.sqlite")

    if not con.open():
        print("Database Error: %s" % con.lastError().databaseText())
        sys.exit(1)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
