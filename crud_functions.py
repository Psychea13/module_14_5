import sqlite3


connection = sqlite3.connect('bot_database.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute(''' CREATE TABLE IF NOT EXISTS Products
        (id INT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INT NOT NULL)''')
    cursor.execute(''' CREATE TABLE IF NOT EXISTS Users
        (id INT PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INT NOT NULL,
        balance INT NOT NULL)''')
    connection.commit()


def add_user(username, email, age):
    cursor.execute(f'INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (f'{username}', f'{email}', f'{age}', 1000))
    connection.commit()


def is_included(username):
    check_user = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    if check_user.fetchone() is None:
        return True
    else:
        return False


def add_product():
    product1 = ['Lay`s Пельмени', 'Шняга шняжная, жизнь общажная..', 100]
    product2 = ['Lay`s Кефир с огурцом', 'Детокс', 200]
    product3 = ['Lay`s Мятный карась', 'Для любителей острых ощущений', 300]
    product4 = ['Lay`s Свежий воздух', 'Для жителей крупных мегаполисов', 400]

    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', product1)
    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', product2)
    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', product3)
    cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', product4)

    connection.commit()


def get_all_products():
    product = cursor.execute('SELECT title, description, price FROM Products').fetchall()
    connection.commit()
    return product


initiate_db()


# add_product()
# add_user('Alex', 'aaa1@gmail.com', 52)
# add_user('Anne', 'aaa2@gmail.com', 12)
# add_user('Bob', 'aaa3@gmail.com', 20)
# add_user('Alice', 'aaa4@gmail.com', 30)
