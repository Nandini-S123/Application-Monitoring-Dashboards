CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    endpoint VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    response_time INT NOT NULL,
    error_type VARCHAR(255)
);