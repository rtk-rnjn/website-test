CREATE TABLE IF NOT EXISTS LOGS (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_level TEXT NOT NULL,
    log_message TEXT NOT NULL,
    log_created_at TEXT NOT NULL
);

-- Path: sql.sql
