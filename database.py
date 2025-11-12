
import sqlite3
from typing import List, Dict, Any

DB_FILE = "books.db"
TABLE_NAME = "llm_books"

#   取得 SQLite 連線，並設定 row_factory 為 sqlite3.Row，以便用欄位名稱存取資料。
def db_connection() :
    #  開啟（或建立）一個叫做 books.db 的 SQLite 資料庫檔案，並回傳一個連線物件 conn
    conn = sqlite3.connect(DB_FILE)
    #  從資料庫讀到「一列」資料時，這列資料會被轉換成 sqlite3.Row 類型
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    #  建立資料表（如果不存在的話），初始化資料庫：initialize_database 函式 
    # id 自動編號主鍵，title 欄位設為 NOT NULL 且 UNIQUE，避免重複書名
    """
    初始化資料庫：如果資料表不存在，則建立之。
    表結構：
      id     INTEGER PRIMARY KEY AUTOINCREMENT
      title  TEXT    NOT NULL UNIQUE
      author TEXT
      price  INTEGER
      link   TEXT
    """
    conn = db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            # id  確保如果表已存在，就不會重複建立
            f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                title  TEXT    NOT NULL UNIQUE,
                author TEXT,
                price  INTEGER,
                link   TEXT
            );
            """
        )

        # conn.commit() 是確保 SQL 指令（CREATE TABLE）送到資料庫並儲存。關閉連線是好習慣，釋放資源、防止鎖檔。

        conn.commit()
    finally:
        conn.close()


def save_books(books: List[Dict[str, Any]]):
    # 批量儲存書籍資料至資料庫。使用 INSERT OR IGNORE 避免重複 title 被寫入。
    # 參數：books: 書籍資料清單，每筆為 dict，包含 keys: "title","author","price","link"
    # 回傳：實際新增的新筆數（忽略已存在的 title）。

    #  如果 books 清單是空的 (if not books:)，直接回傳 0，不做任何儲存
    if not books:
        return 0
    # 確保資料表已建立
    initialize_database()
    conn = db_connection()
    try:
        # 取得連線、游標 (cursor)。查詢目前資料表已有幾筆資料（before_count）
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
        # SQL　SELECT * FROM，取得資料表中所有記錄的數量
        before_count = cursor.fetchone()[0]
        insert_sql = f"""
        INSERT OR IGNORE INTO {TABLE_NAME}
        (title, author, price, link)
        VALUES (?, ?, ?, ?);
        """
        #  SQl 插入語句：INSERT OR IGNORE INTO llm_books (…) VALUES (?, ?, ?)
        # 將 books 清單轉成要插入的資料形式 (data_to_insert)；確保每本書都有 title, author, price, link。
        data_to_insert = [
            (b["title"], b.get("author", ""), b.get("price", 0), b.get("link", ""))
            for b in books
        ]
        #  批量插入

        cursor.executemany(insert_sql, data_to_insert)
        conn.commit()
        # 查詢插入後的資料表筆數 (after_count)

        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
        after_count = cursor.fetchone()[0]

        return after_count - before_count
    finally:
        conn.close()


def query_by_title(keyword):
    # 根據書名關鍵字查詢書籍資料。模糊比對 title 欄位 (LIKE %keyword%)。
    # 回傳：多筆結果，每筆為 dict，包含 keys: title, author, price, link
    
    conn = db_connection()
    try:
        cursor = conn.cursor()
        sql = f"""
        SELECT title, author, price, link
        FROM {TABLE_NAME}
        WHERE title LIKE ?
        ORDER BY title;
        """
        like_pattern = f"%{keyword}%"
        cursor.execute(sql, (like_pattern,))
        rows = cursor.fetchall()

        results: List[Dict[str, Any]] = []
        for row in rows:
            results.append({
                "title": row["title"],
                "author": row["author"],
                "price": row["price"],
                "link": row["link"],
            })
        return results
    finally:
        conn.close()


def query_by_author(keyword) :
    # 根據作者關鍵字查詢書籍資料。模糊比對 author 欄位 (LIKE %keyword%)。
    # 回傳：多筆結果，每筆為 dict，包含 keys: title, author, price, link
    conn = db_connection()
    try:
        cursor = conn.cursor()
        sql = f"""
        SELECT title, author, price, link
        FROM {TABLE_NAME}
        WHERE author LIKE ?
        ORDER BY author;
        """
        like_pattern = f"%{keyword}%"
        cursor.execute(sql, (like_pattern,))
        rows = cursor.fetchall()

        results: List[Dict[str, Any]] = []
        for row in rows:
            results.append({
                "title": row["title"],
                "author": row["author"],
                "price": row["price"],
                "link": row["link"],
            })
        return results
    finally:
        conn.close()


