DROP TABLE IF EXISTS video;

CREATE TABLE video (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  ip TEXT DEFAULT "0.0.0.0",
  url TEXT NOT NULL
);
