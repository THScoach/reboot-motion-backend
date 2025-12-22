-- Fix session unique constraint to allow multiple players per session
-- Drop the old unique constraint on session_id alone
DROP INDEX IF EXISTS ix_sessions_session_id CASCADE;
ALTER TABLE sessions DROP CONSTRAINT IF EXISTS sessions_session_id_key CASCADE;

-- Create composite unique constraint on (session_id, player_id)
ALTER TABLE sessions ADD CONSTRAINT uq_session_player UNIQUE (session_id, player_id);

-- Recreate index on session_id (non-unique)
CREATE INDEX IF NOT EXISTS ix_sessions_session_id ON sessions(session_id);
