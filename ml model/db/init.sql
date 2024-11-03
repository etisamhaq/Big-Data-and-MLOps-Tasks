CREATE DATABASE IF NOT EXISTS Model_Logger;
USE Model_Logger;

CREATE TABLE IF NOT EXISTS Log (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Current_Date_Time DATETIME,
    Input_Params TEXT,
    Output TEXT,
    Response_Time FLOAT
);

-- Grant permissions to mluser
GRANT ALL PRIVILEGES ON Model_Logger.* TO 'mluser'@'%';
FLUSH PRIVILEGES;