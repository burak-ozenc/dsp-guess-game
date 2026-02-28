CREATE TYPE process_status AS ENUM('pending', 'processing', 'completed', 'failed');


CREATE TYPE sound_category AS ENUM ('speech', 'music', 'percussion', 'ambient', 'mechanical', 'nature', 'noise');



CREATE TABLE audio_sources
(
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    audio_source_name TEXT NOT NULL,
    created_at        TIMESTAMPTZ      DEFAULT NOW()
);


CREATE TABLE audio_files
(
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    audio_source_id UUID NOT NULL,
    sample_rate     INT,
    bit_depth       SMALLINT,
    channels        SMALLINT,
    s3_key          VARCHAR,
    s3_bucket       VARCHAR,
    category        VARCHAR,
    subcategory     VARCHAR,
    duration_ms     INT,
    file_name       TEXT NOT NULL,
    file_path       TEXT NOT NULL,
    file_size       BIGINT,
    status          process_status   DEFAULT 'pending',
    created_at      TIMESTAMPTZ      DEFAULT NOW(),
    processed_at    TIMESTAMPTZ,
    file_hash       TEXT NOT NULL,
    CONSTRAINT fk_audio_files_audio_source_id
        FOREIGN KEY (audio_source_id)
            REFERENCES audio_sources (id),
    UNIQUE (file_path),
    UNIQUE (file_hash)
);



CREATE TABLE audio_analytics
(
    id                 UUID        DEFAULT gen_random_uuid(),
    audio_file_id      UUID NOT NULL,
    audio_source_id    UUID NOT NULL,
    -- Analysis params
    hop_length         INT,
    n_fft              INT,
    n_mfcc             SMALLINT,
    -- Time Domain
    rms_energy         JSONB,
    zcr                JSONB,
    crest_factor       FLOAT,
    attack_time_ms     FLOAT,
    autocorr           JSONB,
    -- Spectral
    spectral_centroid  FLOAT,
    spectral_bandwidth FLOAT,
    spectral_rolloff   FLOAT,
    spectral_flatness  FLOAT,
    spectral_flux      JSONB,
    spectral_contrast  JSONB,
    -- Perceptual
    mfcc               JSONB,
    mfcc_mean          JSONB,
    mfcc_variance      JSONB,
    mel_stats_mean     JSONB,
    mel_stats_std      JSONB,
    chroma             JSONB,
    tonnetz            JSONB,
    -- Rhythm
    tempo_bpm          FLOAT,
    tempo_confidence   FLOAT,
    beat_strength      FLOAT,
    onset_density      FLOAT,
    -- Quality
    snr_db             FLOAT,
    silence_ratio      FLOAT,
    clipping_ratio     FLOAT,
    dynamic_range_db   FLOAT,
    thd_percent        FLOAT,
    created_at         TIMESTAMPTZ DEFAULT NOW(),
    source_type        TEXT NOT NULL,
    PRIMARY KEY (id, source_type),
    CONSTRAINT fk_analytics_audio_file
        FOREIGN KEY (audio_file_id)
            REFERENCES audio_files (id),
    CONSTRAINT fk_analytics_audio_source_id
        FOREIGN KEY (audio_source_id)
            REFERENCES audio_sources (id)
) PARTITION BY LIST (source_type);


CREATE TYPE difficulty_level AS ENUM ('easy', 'medium', 'hard');

CREATE TABLE game_sessions
(
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    audio_file_id   UUID             NOT NULL,
    difficulty      difficulty_level NOT NULL,
    hints_used      SMALLINT         DEFAULT 0,
    hints_remaining SMALLINT         NOT NULL,
    user_answer     VARCHAR,
    correct         BOOLEAN,
    score           INT,
    created_at      TIMESTAMPTZ      DEFAULT NOW(),
    answered_at     TIMESTAMPTZ,
    CONSTRAINT fk_session_audio_file
        FOREIGN KEY (audio_file_id)
            REFERENCES audio_files (id)
);

CREATE INDEX idx_game_sessions_audio_file_id ON game_sessions (audio_file_id);
CREATE INDEX idx_game_sessions_difficulty ON game_sessions (difficulty);



CREATE TABLE audio_analytics_music
    PARTITION OF audio_analytics FOR VALUES IN
(
    'music'
);
CREATE TABLE audio_analytics_speech
    PARTITION OF audio_analytics FOR VALUES IN
(
    'speech'
);
CREATE TABLE audio_analytics_noise
    PARTITION OF audio_analytics FOR VALUES IN
(
    'noise'
);



CREATE INDEX idx_audio_files_status ON audio_files (status);


CREATE INDEX idx_audio_files_source_id ON audio_files (audio_source_id);
CREATE INDEX idx_analytics_audio_file_id ON audio_analytics (audio_file_id);