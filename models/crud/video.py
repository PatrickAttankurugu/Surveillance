import sqlite3
import config
from models.schemas import (
    video as video_schemas
)


def get_db_handle():
    conn = sqlite3.connect(config.SQLITE_DB_PATH)
    return conn, conn.cursor()
    

def save_stream(stream_name, stream_type, path_or_link):
    conn, db_cursor = get_db_handle()
    res = db_cursor.execute("INSERT INTO video_streams(name, type, path_or_link) VALUES(?,?,?);", (stream_name, stream_type, path_or_link))
    conn.commit()
    result = res.fetchone()
    conn.close()
    return result


def get_stream_by_id(stream_id):
    conn, db_cursor = get_db_handle()
    db_cursor = db_cursor.execute("SELECT * FROM video_streams WHERE id=?;", (stream_id))
    result = db_cursor.fetchone()
    conn.close()
    return video_schemas.StreamRecord(
        id=result[0],
        name=result[1],
        type=result[2],
        path_or_link=result[3]
    )


def get_stream_by_name(stream_name):
    conn, db_cursor = get_db_handle()
    db_cursor = db_cursor.execute("SELECT * FROM video_streams WHERE name=?;", (stream_name))
    result = db_cursor.fetchone()
    conn.close()
    return video_schemas.StreamRecord(
        id=result[0],
        name=result[1],
        type=result[2],
        path_or_link=result[3]
    )


def get_all_streams():
    conn, db_cursor = get_db_handle()
    db_cursor = db_cursor.execute("SELECT * FROM video_streams")
    result = db_cursor.fetchall()
    conn.close()
    return result