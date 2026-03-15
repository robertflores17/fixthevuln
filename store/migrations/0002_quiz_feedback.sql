-- Quiz feedback tables for FixTheVuln (CyberMoE-inspired RLHF data collection)
-- Per-question events batched at quiz completion via navigator.sendBeacon

CREATE TABLE IF NOT EXISTS quiz_sessions (
  id TEXT PRIMARY KEY,
  quiz_id TEXT NOT NULL,
  total_questions INTEGER NOT NULL,
  correct_count INTEGER NOT NULL,
  score_pct INTEGER NOT NULL,
  time_seconds INTEGER NOT NULL,
  domain_filter TEXT DEFAULT 'all',
  difficulty_filter TEXT DEFAULT 'mixed',
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_session_quiz ON quiz_sessions(quiz_id);
CREATE INDEX IF NOT EXISTS idx_session_created ON quiz_sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_session_score ON quiz_sessions(quiz_id, score_pct);

CREATE TABLE IF NOT EXISTS quiz_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  quiz_id TEXT NOT NULL,
  question_id INTEGER NOT NULL,
  domain INTEGER,
  difficulty TEXT,
  selected_option INTEGER NOT NULL,
  correct_option INTEGER NOT NULL,
  is_correct INTEGER NOT NULL,
  time_ms INTEGER NOT NULL,
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (session_id) REFERENCES quiz_sessions(id)
);

CREATE INDEX IF NOT EXISTS idx_event_session ON quiz_events(session_id);
CREATE INDEX IF NOT EXISTS idx_event_quiz ON quiz_events(quiz_id);
CREATE INDEX IF NOT EXISTS idx_event_question ON quiz_events(quiz_id, question_id);
CREATE INDEX IF NOT EXISTS idx_event_domain ON quiz_events(quiz_id, domain);

-- Classifier feedback table (Phase 3)
CREATE TABLE IF NOT EXISTS classifier_feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  input_text TEXT NOT NULL,
  predicted_domain TEXT NOT NULL,
  confidence REAL,
  is_correct INTEGER NOT NULL,
  correction TEXT,
  entities_json TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_classifier_created ON classifier_feedback(created_at);
CREATE INDEX IF NOT EXISTS idx_classifier_domain ON classifier_feedback(predicted_domain);
