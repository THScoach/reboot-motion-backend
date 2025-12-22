-- Database migration to add new columns to sync_log table
-- Run this SQL against your Railway PostgreSQL database

-- Add new tracking columns to sync_log table
ALTER TABLE sync_log 
ADD COLUMN IF NOT EXISTS players_synced INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS sessions_synced INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS biomechanics_synced INTEGER DEFAULT 0;

-- Verify the changes
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'sync_log'
ORDER BY ordinal_position;
