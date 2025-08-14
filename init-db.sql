-- Language Tutor Database Initialization
-- This script creates all necessary tables for the language learning system

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    native_language VARCHAR(10) NOT NULL DEFAULT 'en',
    target_language VARCHAR(10) NOT NULL DEFAULT 'es',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    preferences JSONB DEFAULT '{}'
);

-- Languages table
CREATE TABLE languages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    native_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Vocabulary table
CREATE TABLE vocabulary (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    language_code VARCHAR(10) NOT NULL,
    word VARCHAR(255) NOT NULL,
    translation VARCHAR(255) NOT NULL,
    part_of_speech VARCHAR(50),
    difficulty_level INTEGER DEFAULT 1,
    frequency_rank INTEGER,
    example_sentence TEXT,
    pronunciation VARCHAR(255),
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (language_code) REFERENCES languages(code)
);

-- User vocabulary progress (spaced repetition)
CREATE TABLE user_vocabulary_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    vocabulary_id UUID NOT NULL,
    ease_factor DECIMAL(3,2) DEFAULT 2.5,
    interval INTEGER DEFAULT 0,
    repetitions INTEGER DEFAULT 0,
    next_review TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_review TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    mastery_level INTEGER DEFAULT 0,
    total_reviews INTEGER DEFAULT 0,
    correct_reviews INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (vocabulary_id) REFERENCES vocabulary(id) ON DELETE CASCADE,
    UNIQUE(user_id, vocabulary_id)
);

-- Learning sessions
CREATE TABLE learning_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    session_type VARCHAR(50) NOT NULL, -- 'review', 'new_words', 'conversation'
    start_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP WITH TIME ZONE,
    words_reviewed INTEGER DEFAULT 0,
    words_correct INTEGER DEFAULT 0,
    session_score DECIMAL(5,2),
    metadata JSONB DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Session vocabulary (many-to-many relationship)
CREATE TABLE session_vocabulary (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL,
    vocabulary_id UUID NOT NULL,
    user_response VARCHAR(255),
    is_correct BOOLEAN,
    response_time_ms INTEGER,
    review_order INTEGER,
    FOREIGN KEY (session_id) REFERENCES learning_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (vocabulary_id) REFERENCES vocabulary(id) ON DELETE CASCADE
);

-- AI conversations
CREATE TABLE ai_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    session_id UUID,
    conversation_start TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    conversation_end TIMESTAMP WITH TIME ZONE,
    language_used VARCHAR(10) NOT NULL,
    difficulty_level INTEGER DEFAULT 1,
    words_used TEXT[],
    new_words_introduced TEXT[],
    conversation_length INTEGER DEFAULT 0,
    user_satisfaction INTEGER,
    metadata JSONB DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES learning_sessions(id) ON DELETE SET NULL
);

-- Conversation messages
CREATE TABLE conversation_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL,
    sender_type VARCHAR(20) NOT NULL, -- 'user' or 'ai'
    message_text TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    vocabulary_used TEXT[],
    difficulty_adjustment INTEGER DEFAULT 0,
    FOREIGN KEY (conversation_id) REFERENCES ai_conversations(id) ON DELETE CASCADE
);

-- Learning goals
CREATE TABLE learning_goals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    goal_type VARCHAR(50) NOT NULL, -- 'daily_words', 'weekly_sessions', 'mastery_level'
    target_value INTEGER NOT NULL,
    current_value INTEGER DEFAULT 0,
    start_date DATE NOT NULL,
    end_date DATE,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- User statistics
CREATE TABLE user_statistics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    date DATE NOT NULL,
    words_reviewed INTEGER DEFAULT 0,
    words_correct INTEGER DEFAULT 0,
    new_words_learned INTEGER DEFAULT 0,
    sessions_completed INTEGER DEFAULT 0,
    total_study_time_minutes INTEGER DEFAULT 0,
    streak_days INTEGER DEFAULT 0,
    accuracy_rate DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, date)
);

-- Create indexes for better performance
CREATE INDEX idx_user_vocabulary_progress_user_id ON user_vocabulary_progress(user_id);
CREATE INDEX idx_user_vocabulary_progress_next_review ON user_vocabulary_progress(next_review);
CREATE INDEX idx_learning_sessions_user_id ON learning_sessions(user_id);
CREATE INDEX idx_ai_conversations_user_id ON ai_conversations(user_id);
CREATE INDEX idx_vocabulary_language_code ON vocabulary(language_code);
CREATE INDEX idx_user_statistics_user_date ON user_statistics(user_id, date);

-- Insert default languages
INSERT INTO languages (code, name, native_name) VALUES
       ('en', 'English', 'English'),
       ('it', 'Italian', 'Italiano'),
       ('es', 'Spanish', 'Español'),
       ('fr', 'French', 'Français'),
       ('de', 'German', 'Deutsch'),
       ('pt', 'Portuguese', 'Português'),
       ('ja', 'Japanese', '日本語'),
       ('ko', 'Korean', '한국어'),
       ('zh', 'Chinese', '中文');

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_user_vocabulary_progress_updated_at 
    BEFORE UPDATE ON user_vocabulary_progress 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create function for spaced repetition calculation (SM-2 algorithm)
CREATE OR REPLACE FUNCTION calculate_next_review(
    p_ease_factor DECIMAL,
    p_interval INTEGER,
    p_repetitions INTEGER,
    p_quality INTEGER
) RETURNS TABLE(
    new_ease_factor DECIMAL,
    new_interval INTEGER,
    next_review_date TIMESTAMP WITH TIME ZONE
) AS $$
DECLARE
    v_new_ease_factor DECIMAL;
    v_new_interval INTEGER;
BEGIN
    -- Calculate new ease factor
    v_new_ease_factor := p_ease_factor + (0.1 - (5 - p_quality) * (0.08 + (5 - p_quality) * 0.02));
    
    -- Ensure ease factor doesn't go below 1.3
    IF v_new_ease_factor < 1.3 THEN
        v_new_ease_factor := 1.3;
    END IF;
    
    -- Calculate new interval
    IF p_repetitions = 0 THEN
        v_new_interval := 1;
    ELSIF p_repetitions = 1 THEN
        v_new_interval := 6;
    ELSE
        v_new_interval := ROUND(p_interval * v_new_ease_factor);
    END IF;
    
    -- Calculate next review date
    RETURN QUERY SELECT 
        v_new_ease_factor,
        v_new_interval,
        CURRENT_TIMESTAMP + (v_new_interval || ' days')::INTERVAL;
END;
$$ LANGUAGE plpgsql; 