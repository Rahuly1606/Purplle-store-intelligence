import sqlite3

conn = sqlite3.connect("store.db")

cursor = conn.cursor()

cursor.execute("""
SELECT
event_id,
store_id,
visitor_id,
event_type
FROM events
""")

for row in cursor.fetchall():
    print(row)

conn.close()