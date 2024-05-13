import sqlite3


class Database:
    def __init__(self):
        try:
            self.connection = sqlite3.connect('hangman.db')
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(e)

    def create_users_table(self):
        with self.connection as conn:
            cur = conn.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            score INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            try:
                cur.execute(query)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)

    def create_words_table(self):
        with self.connection as conn:
            cur = conn.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS words(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE
            )
            """
            try:
                cur.execute(query)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)

    def create_games_table(self):
        with self.connection as conn:
            cur = conn.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS games(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            word_id INTEGER NOT NULL,
            won INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE
            )
            """
            try:
                cur.execute(query)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)

    def insert_user(self, username, password):
        with self.connection as conn:
            cur = conn.cursor()
            query = """
            INSERT INTO users(username, password) values (?,?)
            """
            try:
                cur.execute(query, (username, password))
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)

    def insert_word(self, word):
        with self.connection as conn:
            cur = conn.cursor()
            query = """
            INSERT INTO words(word) values (?)
            """
            try:
                cur.execute(query, (word,))
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)

    def insert_game(self, user_id, word_id, won):
        with self.connection as conn:
            cur = conn.cursor()
            query = """
            INSERT INTO games(user_id, word_id, won) values (?,?,?)
            """
            try:
                cur.execute(query, (user_id, word_id, won))
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)

    def get_user(self, username):
        with self.connection as conn:
            cur = conn.cursor()
            query = """
            SELECT * FROM users WHERE username = ?
            """
            try:
                cur.execute(query, (username,))
                row = cur.fetchone()
                if row is None:
                    return None
                return row
            except Exception as e:
                conn.rollback()
                print(e)

    def get_word(self, word):
        with self.connection as conn:
            cur = conn.cursor()
            query = """
            SELECT * FROM words WHERE word = ?
            """
            try:
                cur.execute(query, (word,))
                row = cur.fetchone()
                if row is None:
                    return None
                return row
            except Exception as e:
                conn.rollback()
                print(e)

    def update_user_score(self, user_id, score):
        with self.connection as conn:
            cur = conn.cursor()
            query = """
            UPDATE users SET score = score + ? WHERE id = ?
            """
            try:
                cur.execute(query, (score, user_id))
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)

    def get_all_words(self):
        with self.connection as conn:
            cur = conn.cursor()
            query = """
            SELECT word FROM words
            """
            try:
                cur.execute(query)
                rows = cur.fetchall()
                # Convert list of tuples to list of strings
                words = [row[0] for row in rows]
                return words
            except Exception as e:
                conn.rollback()
                print(e)

    def close_connection(self):
        self.connection.close()
