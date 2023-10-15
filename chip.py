import sqlite3

# Verbindung zur Datenbank herstellen (oder erstellen, falls sie nicht existiert)
conn = sqlite3.connect('entry_system.db')
cursor = conn.cursor()

# Tabelle erstellen, um die Chips und deren Status zu speichern
cursor.execute('''
CREATE TABLE IF NOT EXISTS chips (
    id INTEGER PRIMARY KEY,
    chip_id TEXT,
    is_registered INTEGER
)
''')
conn.commit()

def register_chip(chip_id):
    cursor.execute('INSERT INTO chips (chip_id, is_registered) VALUES (?, 1)', (chip_id,))
    conn.commit()
    print(f"Chip '{chip_id}' wurde registriert.")

def check_chip_status(chip_id):
    cursor.execute('SELECT is_registered FROM chips WHERE chip_id = ?', (chip_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

def main():
    while True:
        user_input = input("Bitte scannen Sie Ihren Chip: ")
        
        chip_status = check_chip_status(user_input)
        
        if chip_status is not None:
            if chip_status == 1:
                print("Zugang gewährt! Grünes Licht.")
            else:
                print("Ihr Chip ist bereits registriert, aber deaktiviert.")
        else:
            print("Ihr Chip ist nicht registriert. Möchten Sie ihn registrieren? (j/n)")
            choice = input()
            if choice.lower() == "j":
                register_chip(user_input)
            else:
                print("Zugang verweigert.")
    
if __name__ == "__main__":
    main()
