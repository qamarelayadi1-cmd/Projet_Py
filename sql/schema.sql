CREATE TABLE IF NOT EXISTS attempts (
    id BIGSERIAL PRIMARY KEY,
    log_month VARCHAR(3) NOT NULL,
    log_day INTEGER NOT NULL,
    log_time TIME NOT NULL,
    server VARCHAR(100),
    service VARCHAR(50),
    process_id INTEGER,
    username VARCHAR(255),
    ip INET NOT NULL,
    port INTEGER,
    status VARCHAR(10) NOT NULL CHECK (status IN ('SUCCESS', 'FAILED')),
    invalid_user BOOLEAN NOT NULL DEFAULT FALSE,
    country VARCHAR(10) NOT NULL DEFAULT 'Unknown',
    attempt_count INTEGER NOT NULL DEFAULT 1,
    raw_line TEXT NOT NULL UNIQUE
);
