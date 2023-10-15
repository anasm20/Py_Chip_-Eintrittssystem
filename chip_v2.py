import sqlite3
import time

class EntrySystem:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.create_tables()
        self.cursor = self.conn.cursor()
        self.current_chip_id = 1000  # Startwert für die Chip-ID

    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                chip_id INTEGER PRIMARY KEY,
                username TEXT
            )
        ''')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS access_logs (
                access_id INTEGER PRIMARY KEY,
                chip_id INTEGER,
                access_time TIMESTAMP
            )
        ''')
        self.conn.commit()

    def register_user(self, username):
        # Generiere eine eindeutige Chip-ID und erhöhe die aktuelle Chip-ID
        chip_id = self.current_chip_id
        self.current_chip_id += 1
        self.cursor.execute("INSERT INTO users (chip_id, username) VALUES (?, ?)", (chip_id, username))
        self.conn.commit()
        return f"User registered successfully. Your chip ID is {chip_id}"

    def check_access(self, chip_id):
        self.cursor.execute("SELECT * FROM users WHERE chip_id = ?", (chip_id,))
        user = self.cursor.fetchone()
        if user:
            username = user[1]
            access_time = self.get_current_time()
            self.cursor.execute("INSERT INTO access_logs (chip_id, access_time) VALUES (?, ?)", (chip_id, access_time))
            self.conn.commit()
            return f"Access granted for user: {username}"
        return "Access denied"

    def get_current_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')

def main():
    database_name = 'entry_system.db'
    entry_system = EntrySystem(database_name)

    while True:
        #print("Willkommen in Chip_Eintrittssystem. Wähle 1,2 oder 3")
        print("1. Register User")
        print("2. Check Access")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            result = entry_system.register_user(username)
            print(result)

        elif choice == "2":
            chip_id = int(input("Enter chip ID: "))
            result = entry_system.check_access(chip_id)
            print(result)

        elif choice == "3":
            entry_system.conn.close()
            print("Exiting the Entry System")
            break

if __name__ == '__main__':
    main()
