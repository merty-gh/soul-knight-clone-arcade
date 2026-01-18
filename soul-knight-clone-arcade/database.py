import sqlite3
import config

DB_NAME = "gamedata.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Таблица игрока
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY,
            crystals INTEGER DEFAULT 0
        )
    ''')

    # Таблица скинов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unlocked_skins (
            skin_name TEXT PRIMARY KEY
        )
    ''')

    # --- НОВОЕ: Таблица оружия ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unlocked_weapons (
            weapon_name TEXT PRIMARY KEY
        )
    ''')

    cursor.execute('SELECT count(*) FROM player')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO player (id, crystals) VALUES (1, 0)')
        cursor.execute('INSERT INTO unlocked_skins (skin_name) VALUES (?)', ("Adventurer",))
        # Пистолет доступен сразу
        cursor.execute('INSERT INTO unlocked_weapons (weapon_name) VALUES (?)', ("Pistol",))

    conn.commit()
    conn.close()


# ... (Функции get_crystals, add_crystals, spend_crystals - ОСТАВИТЬ КАК БЫЛО) ...
def get_crystals():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT crystals FROM player WHERE id=1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def add_crystals(amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE player SET crystals = crystals + ? WHERE id=1', (amount,))
    conn.commit()
    conn.close()


def spend_crystals(amount):
    current = get_crystals()
    if current >= amount:
        add_crystals(-amount)
        return True
    return False


def get_unlocked_skins():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT skin_name FROM unlocked_skins')
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def unlock_skin(skin_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO unlocked_skins (skin_name) VALUES (?)', (skin_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()


# --- НОВЫЕ ФУНКЦИИ ДЛЯ ОРУЖИЯ ---
def get_unlocked_weapons():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT weapon_name FROM unlocked_weapons')
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def unlock_weapon(weapon_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO unlocked_weapons (weapon_name) VALUES (?)', (weapon_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()


init_db()