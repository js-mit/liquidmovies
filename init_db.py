import sqlite3
import pathlib

conn = sqlite3.connect("instance/liquid.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)

with open(pathlib.Path(__file__).parent/'schema.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()

cur.execute("INSERT INTO video (url, ip) VALUES (?, ?)",
            ("https://google.com", "0.0.0.0")
            )

cur.execute("INSERT INTO video (url, ip) VALUES (?, ?)",
            ("https://microsoft.com", "0.0.0.0")
            )

conn.commit()
conn.close()
