import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            code TEXT PRIMARY KEY,
            title TEXT,
            category TEXT,
            category_label TEXT,
            genre TEXT,
            year TEXT,
            language TEXT,
            file_id TEXT,
            views INTEGER DEFAULT 0
        )
        """)

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT
        )
        """)

        self.conn.commit()

    def add_user(self, user_id, username, first_name):
        self.cur.execute(
            "INSERT OR IGNORE INTO users VALUES (?, ?, ?)",
            (user_id, username, first_name)
        )
        self.conn.commit()

    def get_all_users(self):
        return self.cur.execute("SELECT * FROM users").fetchall()

    def add_movie(self, code, title, category, category_label,
                  genre, year, language, file_id):

        try:
            self.cur.execute("""
            INSERT INTO movies
            (code,title,category,category_label,genre,year,language,file_id)
            VALUES (?,?,?,?,?,?,?,?)
            """, (
                code, title, category, category_label,
                genre, year, language, file_id
            ))
            self.conn.commit()
            return True
        except:
            return False

    def get_movie_by_code(self, code):
        return self.cur.execute(
            "SELECT * FROM movies WHERE code=?",
            (code,)
        ).fetchone()

    def increment_views(self, code):
        self.cur.execute(
            "UPDATE movies SET views=views+1 WHERE code=?",
            (code,)
        )
        self.conn.commit()

    def get_all_movies(self):
        return self.cur.execute("SELECT * FROM movies").fetchall()

    def get_recent_movies(self, limit):
        return self.cur.execute(
            "SELECT * FROM movies ORDER BY rowid DESC LIMIT ?",
            (limit,)
        ).fetchall()

    def get_movies_by_category(self, cat):
        return self.cur.execute(
            "SELECT * FROM movies WHERE category=?",
            (cat,)
        ).fetchall()

    def delete_movie(self, code):
        self.cur.execute(
            "DELETE FROM movies WHERE code=?",
            (code,)
        )
        self.conn.commit()
        return self.cur.rowcount > 0

    def get_stats(self):
        users = self.cur.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

        movies = self.cur.execute(
            "SELECT COUNT(*) FROM movies"
        ).fetchone()[0]

        views = self.cur.execute(
            "SELECT SUM(views) FROM movies"
        ).fetchone()[0] or 0

        top = self.cur.execute("""
        SELECT code,title,views
        FROM movies
        ORDER BY views DESC
        LIMIT 5
        """).fetchall()

        return {
            "users": users,
            "movies": movies,
            "views": views,
            "top": top
        }