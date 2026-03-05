-- Error logging tables for FixTheVuln
CREATE TABLE IF NOT EXISTS error_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  message TEXT NOT NULL,
  source TEXT DEFAULT '',
  lineno INTEGER DEFAULT 0,
  colno INTEGER DEFAULT 0,
  stack TEXT DEFAULT '',
  page TEXT DEFAULT '',
  user_agent TEXT DEFAULT '',
  ip TEXT DEFAULT '',
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_error_created ON error_log(created_at);
CREATE INDEX IF NOT EXISTS idx_error_message ON error_log(message);

CREATE TABLE IF NOT EXISTS error_alert_sent (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  message_hash TEXT NOT NULL,
  sent_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_alert_hash ON error_alert_sent(message_hash, sent_at);
