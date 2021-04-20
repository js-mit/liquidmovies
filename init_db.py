import sqlite3
import pathlib

schema_path = str(pathlib.Path(__file__).parent/"liquid/schema.sql")
db_path = str(pathlib.Path(__file__).parent/"instance/liquid.sqlite")

conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)

# load up the schema
with open(schema_path) as f:
    conn.executescript(f.read())

# insert dummy entries
cur = conn.cursor()

cur.execute(
    "INSERT INTO video (url, ip) VALUES (?, ?)",
    ("https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4", "0.0.0.0")
)

cur.execute(
    "INSERT INTO video (url, ip) VALUES (?, ?)",
    ("https://vjs.zencdn.net/v/oceans.mp4", "0.0.0.0")
)

cur.execute(
    "INSERT INTO video (url, ip) VALUES (?, ?)", ("http://localhost:9004/mit_test.mp4", "0.0.0.0")
)

cur.execute(
    "INSERT INTO liquid (video, liquid, method, desc) VALUES (?, ?, ?, ?)", (2, "[{start: 3, stop: 5}, {start: 20, stop: 23}, {start: 35, stop: 38}]", 1, "fake bookmark")
)

conn.commit()
conn.close()
