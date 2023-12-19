import sqlite3
class ClothingStoreDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('clothing_store.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS clothes
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           brand TEXT NOT NULL,
                           quantity INTEGER NOT NULL)''')

        cursor.execute("INSERT INTO clothes (name, brand, quantity) VALUES (?, ?, ?)",
                       ('T-shirt', 'Nike', 50))
        cursor.execute("INSERT INTO clothes (name, brand, quantity) VALUES (?, ?, ?)",
                       ('Jeans', 'Levi\'s', 30))

        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL,
                           password TEXT NOT NULL,
                           role TEXT NOT NULL)''')
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                        ('user', '12345', 'user'))
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                        ('admin', 'admin123', 'admin'))

        self.connection.commit()

    def validate_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            return user[3]
        else:
            return None

    def get_clothes(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM clothes")
        return cursor.fetchall()

    def add_clothes(self, name, brand, quantity):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO clothes (name, brand, quantity) VALUES (?, ?, ?)",
                       (name, brand, quantity))
        self.connection.commit()

    def update_password_admin(self, password, name):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (password, name))
        self.connection.commit()

    def update_clothes_quantity(self, clothes_id, new_quantity):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE clothes SET quantity = ? WHERE id = ?", (new_quantity, clothes_id))
        self.connection.commit()

    def delete_clothes(self, clothes_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM clothes WHERE id = ?", (clothes_id,))
        self.connection.commit()

class ClothesItem:
    def __init__(self, name, brand, quantity):
        self.name = name
        self.brand = brand
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} - {self.brand} ({self.quantity} pcs.)"

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class ClothingStore:
    def __init__(self, database):
        self.database = database
        self.current_user = User('', '', '')

    def login(self, username, password):
        role = self.database.validate_user(username, password)
        if role:
            self.current_user = User(username, password, role)
            print('Авторизация прошла успешно.')
        else:
            print('Ошибка авторизации.')

    def change_password_admin(self, new_password, name):
        if self.current_user.role == 'admin':
            self.database.update_password_admin(new_password, name)
            print('Пароль успешно обновлен.')
        else:
            print('Ошибка доступа. Только администраторы могут обновлять пароли.')

    def add_clothes(self, name, brand, quantity):
        if self.current_user.role == 'admin':
            self.database.add_clothes(name, brand, quantity)
            print('Одежда успешно добавлена в магазин.')
        else:
            print('Ошибка доступа. Добавлять одежду могут только администраторы.')

    def delete_clothes(self, clothes_id):
        if self.current_user.role == 'admin':
            self.database.delete_clothes(clothes_id)
            print('Одежда успешно удалена из магазина.')
        else:
            print('Ошибка доступа. Удалять одежду могут только администраторы.')

    def show_clothes(self):
        clothes = self.database.get_clothes()
        for cloth in clothes:
            cloth_obj = ClothesItem(cloth[1], cloth[2], cloth[3])
            print(cloth_obj)

    def update_clothes_quantity(self, clothes_id, new_quantity):
        if self.current_user.role == 'admin':
            self.database.update_clothes_quantity(clothes_id, new_quantity)
            print('Количество одежды успешно обновлено.')
        else:
            print('Ошибка доступа. Только администраторы могут обновлять количество одежды.')

database = ClothingStoreDatabase()

c = 2
clothes_ids = 0
clothing_store = ClothingStore(database)
print("Введите имя пользователя:")
name = input()
print("Введите пароль:")
password = input()
clothing_store.login(name, password)

while True:
    if name == "admin":
        print("Что хотите сделать?")
        print("1. Сменить пароль")
        print("2. Удалить одежду из реестра")
        print("3. Добавить одежду в реестр")
        print("4. Выход")

        answer = input("Выберите команду: ")
        match answer:
            case "1":
                print("Введите новый пароль")
                new_password = input()
                clothing_store.change_password_admin(new_password, name)
            case "2":
                for i in range(c, clothes_ids):
                    clothing_store.delete_clothes(i)
                continue
            case "3":
                clothing_store.add_clothes('Худи', 'Адидас', 20)
                c = c + 1
                clothes_ids = c
                continue
            case "4":
                for i in range(c, clothes_ids):
                    clothing_store.delete_clothes(i)
                break
            case _:
                print("Invalid command!")
    clothing_store.show_clothes()
    clothing_store.update_clothes_quantity(1, 8)
    clothing_store.delete_clothes(2)