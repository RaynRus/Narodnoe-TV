import sqlite3
import datetime

db_name = "nartv.db"


def create_video_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS video (
            id INTEGER PRIMARY KEY,
            title TEXT,
            text TEXT,
            file_name VARCHAR(255),
            at_publish TEXT,
            author_id INTEGER
        )
    """
    con = sqlite3.connect(db_name)
    con.execute(SQL)


class Video:
    def __init__(self, id, title, text, file_name, at_publish, author_id, username=None):
        self.id = id
        self.title = title
        self.text = text
        self.file_name = file_name
        self.at_publish = at_publish
        self.author_id = author_id
        self.author_username = username

    @staticmethod
    def get_all():
        SQL = """
               SELECT video.*, user.username FROM video
               LEFT JOIN user ON user.id = video.author_id
        """

        con = sqlite3.connect(db_name)
        q = con.execute(SQL)
        data = q.fetchall()
        return [Video(*row) for row in data]

    @staticmethod
    def get_by_author(author_id):
        SQL = "SELECT * FROM video WHERE author_id = ?"
        con = sqlite3.connect(db_name)
        q = con.execute(SQL, [author_id])
        data = q.fetchall()
        return [Video(*row) for row in data]

    @staticmethod
    def create(title, text, file_name, author_id):
        SQL = """
            INSERT INTO video(title, text, file_name, at_publish, author_id)
            VALUES (?, ?, ?, ?, ?)
        """
        con = sqlite3.connect(db_name)
        con.execute(SQL, [
            title, text, file_name, datetime.datetime.now().strftime("%d.%m.%Y %H:%M"), author_id
        ])
        con.commit()
