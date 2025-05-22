import sqlite3

class DatabaseManager:
    def __init__(self, db_name="soru_bankasi.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sorular (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                soru TEXT,
                secenekA TEXT,
                secenekB TEXT,
                secenekC TEXT,
                secenekD TEXT,
                secenekE TEXT,
                dogru_cevap TEXT
            )
        """)
        self.connection.commit()

    def soru_ekle(self, soru, a, b, c, d, e, dogru_cevap):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO sorular (soru, secenekA, secenekB, secenekC, secenekD, secenekE, dogru_cevap)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (soru, a, b, c, d, e, dogru_cevap))
        self.connection.commit()

    def tum_sorulari_getir(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM sorular")
        return cursor.fetchall()

    def dataframe_olarak_getir(self):
        import pandas as pd
        df = pd.read_sql_query("SELECT * FROM sorular", self.connection)
        return df

    def close(self):
        self.connection.close()
