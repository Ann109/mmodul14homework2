import sqlite3

connection = sqlite3.connect('not_telegram')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER,
        balance INTEGER NOT NULL
    )
''')

cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')

for i in range(1, 10):
    cursor.execute(
        'INSERT INTO Users (username, email, age, balance) '
            'VALUES (?, ?, ?, ?)',
        (f'User{i}', f'example{i}@gmail.com', f'{(i + 1)*10}', 1000))

for i in range(1, 10):
    if i % 2:  # каждая 2-я запись начиная с 1-й
        cursor.execute(
            'UPDATE Users SET balance = 500 WHERE id = ?',
            (i,))

for i in range(1, 10):
    if i % 3 == 1:  # каждая 3-я запись начиная с 1-й
        cursor.execute(
            'DELETE FROM Users WHERE id = ?',
            (i,))

# Удаление из базы данных not_telegram.db запись с id = 6
cursor.execute('DELETE FROM Users WHERE id = 6')

# Общее количество записей
cursor.execute('SELECT COUNT(*) FROM Users')
text = cursor.fetchone()[0]
print(text)

# Сумма всех балансов
cursor.execute('SELECT SUM(balance) FROM Users')
all_balances = cursor.fetchone()[0]
print(all_balances)

# Средний баланс
cursor.execute('SELECT SUM(balance) FROM Users')
all_balance = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()[0]
print(all_balance/total_users)


cursor.execute("SELECT * FROM Users WHERE age <> 60")
users = cursor.fetchall()
for user in users:
    id, username, email, age, balance = user
    print(f'Имя: {username} | '
          f'Почта: {email} | '
          f'Возраст: {age} | '
          f'Баланс: {balance}')

connection.commit()
connection.close()