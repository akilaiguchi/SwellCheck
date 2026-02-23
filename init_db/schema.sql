CREATE DATABASE IF NOT EXISTS swellcheck;
USE swellcheck;

-- Directory
-- Store static info about each station
CREATE TABLE IF NOT EXISTS buoys (
    buoy_id INT PRIMARY KEY,
    location_name VARCHAR(100) NOT NULL,
    latitude FLOAT,
    longitude FLOAT
);


-- Time-series data
-- store growing list of buoy measurements
CREATE TABLE IF NOT EXISTS readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    buoy_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    wvht FLOAT,
    swh FLOAT,
    swp FLOAT,
    wwh FLOAT,
    wwp FLOAT,
    swd VARCHAR(3),
    wwd VARCHAR(3),
    steepness VARCHAR(10),
    apd FLOAT,
    mwd SMALLINT,

    -- link readings back to buoy directory
    -- if a buoy is deleted from 'buoys' table, its readings are also deleted
    CONSTRAINT fk_buoy
        FOREIGN KEY (buoy_id)
        REFERENCES buoys(buoy_id)
        ON DELETE CASCADE,
    UNIQUE KEY uq_buoy_timestamp (buoy_id, timestamp)
);

-- Install initial data (add rows as needed)
-- INSERT IGNORE INTO buoys (buoy_id, location_name, latitude, longitude)
-- VALUES (12345, 'Scripps', 32.87, -117.26);
INSERT IGNORE INTO buoys (buoy_id, location_name, latitude, longitude)
VALUES (51205, 'Pauwela, Maui, HI', 21.018, -156.421);

