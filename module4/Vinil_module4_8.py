import sqlite3
DB = "Vinil_module4_2.db"
def search_description(term, db_path=DB, limit=10):
    """Find best description matches using case-insensitive substring relevance."""
    pattern = f"%{term}%"
    with sqlite3.connect(db_path) as connection:
        return connection.execute(
            """SELECT * FROM tasks WHERE description LIKE ?
               ORDER BY CASE WHEN lower(description)=lower(?) THEN 0
                             WHEN lower(description) LIKE lower(?) THEN 1 ELSE 2 END, id LIMIT ?""",
            (pattern, term, f"{term}%", limit)).fetchall()
if __name__ == "__main__":
    print(search_description(input("Search descriptions: ")))
