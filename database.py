#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path="davxtv.db"):
        self.db_path = db_path
        self._init()

    def _conn(self):
        c = sqlite3.connect(self.db_path)
        c.row_factory = sqlite3.Row
        return c

    def _init(self):
        with self._conn() as c:
            c.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id    INTEGER PRIMARY KEY,
                    username   TEXT DEFAULT '',
                    first_name TEXT DEFAULT '',
                    lang       TEXT DEFAULT 'uz',
                    joined_at  TEXT DEFAULT (datetime('now'))
                );

                CREATE TABLE IF NOT EXISTS movies (
                    code           TEXT PRIMARY KEY,
                    title          TEXT NOT NULL,
                    category       TEXT NOT NULL,
                    genre          TEXT DEFAULT '-',
                    year           TEXT DEFAULT '-',
                    language       TEXT DEFAULT '-',
                    file_id        TEXT NOT NULL,
                    views          INTEGER DEFAULT 0,
                    added_at       TEXT DEFAULT (datetime('now'))
                );
            """)
        logger.info("✅ DB tayyor")

    # ── USERS ──────────────────────────────────────────────────────────────────
    def add_user(self, user_id, username="", first_name=""):
        with self._conn() as c:
            c.execute(
                "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?,?,?)",
                (user_id, username, first_name)
            )

    def get_user_lang(self, user_id):
        with self._conn() as c:
            row = c.execute("SELECT lang FROM users WHERE user_id=?", (user_id,)).fetchone()
            return row["lang"] if row else None   # None = til tanlanmagan

    def set_user_lang(self, user_id, lang):
        with self._conn() as c:
            c.execute("UPDATE users SET lang=? WHERE user_id=?", (lang, user_id))

    def get_all_users(self):
        with self._conn() as c:
            return [dict(r) for r in c.execute("SELECT * FROM users").fetchall()]

    # ── MOVIES ─────────────────────────────────────────────────────────────────
    def add_movie(self, code, title, category, genre, year, language, file_id):
        try:
            with self._conn() as c:
                c.execute(
                    "INSERT INTO movies (code,title,category,genre,year,language,file_id) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (code.upper(), title, category.upper(), genre, year, language, file_id)
                )
            return True
        except sqlite3.IntegrityError:
            return False   # kod allaqachon bor

    def delete_movie(self, code):
        with self._conn() as c:
            cur = c.execute("DELETE FROM movies WHERE code=?", (code.upper(),))
            return cur.rowcount > 0

    def get_movie(self, code):
        with self._conn() as c:
            row = c.execute("SELECT * FROM movies WHERE code=?", (code.upper(),)).fetchone()
            return dict(row) if row else None

    def get_all_movies(self):
        with self._conn() as c:
            return [dict(r) for r in c.execute(
                "SELECT * FROM movies ORDER BY category, code"
            ).fetchall()]

    def get_by_category(self, cat):
        with self._conn() as c:
            return [dict(r) for r in c.execute(
                "SELECT * FROM movies WHERE category=? ORDER BY code", (cat.upper(),)
            ).fetchall()]

    def get_recent(self, n=10):
        with self._conn() as c:
            return [dict(r) for r in c.execute(
                "SELECT * FROM movies ORDER BY added_at DESC LIMIT ?", (n,)
            ).fetchall()]

    def inc_views(self, code):
        with self._conn() as c:
            c.execute("UPDATE movies SET views=views+1 WHERE code=?", (code.upper(),))

    def stats(self):
        with self._conn() as c:
            users  = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            movies = c.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
            views  = c.execute("SELECT COALESCE(SUM(views),0) FROM movies").fetchone()[0]
            top    = [dict(r) for r in c.execute(
                "SELECT code,title,views FROM movies ORDER BY views DESC LIMIT 5"
            ).fetchall()]
        return {"users": users, "movies": movies, "views": views, "top": top}
