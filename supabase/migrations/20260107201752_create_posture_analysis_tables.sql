/*
  # Create Posture Analysis Tables

  ## Overview
  This migration creates the database schema for the Kuro Performance Posture Analysis application.
  
  ## Tables Created
  
  ### 1. user_sessions
  - `id` (uuid, primary key) - Unique session identifier
  - `name` (text) - User's name
  - `height` (numeric) - User's height in mm
  - `created_at` (timestamptz) - Session creation timestamp
  
  ### 2. analysis_results
  - `id` (uuid, primary key) - Unique analysis identifier
  - `session_id` (uuid, foreign key) - References user_sessions
  - `analysis_type` (text) - Type of analysis (back_front_analysis or side_analysis)
  - `classification` (text) - Posture classification (Normal, Kyphosis, Lordosis, Swayback)
  - `confidence` (numeric) - Confidence score (0-1)
  - `score` (numeric) - Overall posture score (0-100)
  - `measurements` (jsonb) - JSON object containing all measurements
  - `keypoints` (jsonb) - JSON object containing detected keypoints
  - `image_path` (text) - Path to analyzed image
  - `created_at` (timestamptz) - Analysis timestamp
  
  ## Security
  - RLS enabled on all tables
  - Public read/write access (for standalone app usage)
  - Can be restricted later for multi-user web deployment
  
  ## Notes
  - Uses UUID for primary keys for better scalability
  - JSONB for flexible storage of measurements and keypoints
  - Timestamps with timezone for accurate time tracking
*/

CREATE TABLE IF NOT EXISTS user_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  height numeric NOT NULL CHECK (height > 0),
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS analysis_results (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id uuid REFERENCES user_sessions(id) ON DELETE CASCADE,
  analysis_type text NOT NULL,
  classification text NOT NULL,
  confidence numeric CHECK (confidence >= 0 AND confidence <= 1),
  score numeric CHECK (score >= 0 AND score <= 100),
  measurements jsonb DEFAULT '{}'::jsonb,
  keypoints jsonb DEFAULT '{}'::jsonb,
  image_path text,
  created_at timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_analysis_session ON analysis_results(session_id);
CREATE INDEX IF NOT EXISTS idx_analysis_created ON analysis_results(created_at DESC);

ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE analysis_results ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access to user_sessions"
  ON user_sessions FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Allow public insert to user_sessions"
  ON user_sessions FOR INSERT
  TO public
  WITH CHECK (true);

CREATE POLICY "Allow public read access to analysis_results"
  ON analysis_results FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Allow public insert to analysis_results"
  ON analysis_results FOR INSERT
  TO public
  WITH CHECK (true);
