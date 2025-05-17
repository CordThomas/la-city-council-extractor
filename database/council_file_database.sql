--
-- File generated with SQLiteStudio v3.4.4 on Fri May 16 09:45:34 2025
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: council_action
CREATE TABLE council_action (
    council_action_id INTEGER     PRIMARY KEY AUTOINCREMENT,
    cf_number         TEXT (10)   REFERENCES council_file (cf_number),
    action_date       TEXT (10),
    description       TEXT (1000) 
);


-- Table: council_distance_matrix
CREATE TABLE council_distance_matrix (
    council_distance_matrix_id INTEGER PRIMARY KEY AUTOINCREMENT,
    council_n1                 INTEGER,
    council_n2                 INTEGER,
    distance                   INTEGER
);


-- Table: council_district
CREATE TABLE council_district (
    district_n INTEGER    PRIMARY KEY,
    district   TEXT (100) 
);


-- Table: council_district_member
CREATE TABLE council_district_member (
    council_district_member_id INTEGER    PRIMARY KEY AUTOINCREMENT,
    district_n                 INTEGER    REFERENCES council_district (district_n),
    name_last                  TEXT (40),
    name_first                 TEXT (40),
    start_date                 DATE,
    end_date                   DATE,
    mover_name                 TEXT (100) 
);


-- Table: council_document
CREATE TABLE council_document (
    cf_document_id INTEGER    PRIMARY KEY AUTOINCREMENT,
    cf_number      TEXT (10)  REFERENCES council_file (cf_number),
    action_date    TEXT (10),
    title          TEXT (100),
    file_name      TEXT (100) 
);


-- Table: council_document_text
CREATE TABLE council_document_text (
    cf_document_id   INT          REFERENCES council_document (cf_document_id),
    cf_document_text TEXT (65535) 
);


-- Table: council_file
CREATE TABLE council_file (
    cf_number           TEXT (10)   PRIMARY KEY
                                    UNIQUE
                                    NOT NULL,
    council_district    INTEGER,
    direct_to_council   TEXT (1),
    date_expiration     TEXT (10),
    date_last_changed   TEXT (10),
    date_received       TEXT (10),
    initiated_by        TEXT (40),
    mover               TEXT (40),
    mover_comment       TEXT (256),
    pending_committee   TEXT (100),
    reference_recs      TEXT (400),
    second              TEXT (40),
    title               TEXT (256),
    reward_amount       TEXT (20),
    reward_duration     TEXT (20),
    reward_publish_date TEXT (20),
    reward_expire_date  TEXT (20),
    subject             TEXT (1000) 
);


-- Table: council_file_district
CREATE TABLE council_file_district (
    council_file_district_id INTEGER   PRIMARY KEY
                                       UNIQUE
                                       NOT NULL,
    cf_number                TEXT (10) REFERENCES council_file (cf_number),
    district_n               INTEGER   REFERENCES council_district (district_n) 
);


-- Table: council_file_legislative_topic
CREATE TABLE council_file_legislative_topic (
    council_file_legislative_topic INTEGER   PRIMARY KEY AUTOINCREMENT,
    cf_number                      TEXT (10) REFERENCES council_file (cf_number),
    topic_id                       INTEGER   REFERENCES legislative_topic (topic_id) 
);


-- Table: council_vote
CREATE TABLE council_vote (
    cf_number    TEXT (10) PRIMARY KEY
                           UNIQUE
                           REFERENCES council_file (cf_number),
    meeting_date TEXT (10),
    meeting_type TEXT (20),
    vote_action  TEXT (20) 
);


-- Table: council_vote_result
CREATE TABLE council_vote_result (
    council_vote_result_id INTEGER   PRIMARY KEY AUTOINCREMENT,
    cf_number              TEXT (10),
    council_district       INTEGER,
    council_member         TEXT (40),
    vote                   TEXT (10) 
);


-- Table: legislative_topic
CREATE TABLE legislative_topic (
    topic_id        INTEGER   PRIMARY KEY,
    topic_label     TEXT (40),
    topic_keyphrase TEXT (40) 
);


-- View: council_documents_cleaned_inner_1_v
CREATE VIEW council_documents_cleaned_inner_1_v AS
    SELECT substr(action_date, 7, 10) AS action_year,
           action_date,
           replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(title, 'Voices Neighborhood Council', 'Voices of 90037 Neighborhood Council'), 'Community Impact Statement from', ''), 'Community Impact Statement submitted by ', ''), ' Community Council', ''), ' Neighborhood Council', ''), ' (e)', ''), 'Bel-Air Beverly', 'Bel Air-Beverly'), 'Community Impact Statement submitted by', ''), 'Neighbhood Council', ''), ' ofs', ''), '- 2nd Submission', ''), 'Neightborhood Council', '') AS council,
           file_name
      FROM council_document
     WHERE title LIKE 'Community Impact Statement from%' OR 
           title LIKE 'Community Impact Statement submitted by%';


-- View: council_documents_cleaned_inner_2_v
CREATE VIEW council_documents_cleaned_inner_2_v AS
    SELECT action_year,
           action_date,
           replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(council, 'Community Impact Statement Submitted by ', ''), 'Historic Cultural North,Historic Cultural North', 'Historic Cultural North'), 'neighborhood Council', ''), 'NC', ''), 'Neighborhood Council of', ''), 'Neighborhood Council', ''), 'Neighbhorhood Council', ''), 'United Neighborhoods of the ', ''), 'NDC', ''), '(EH)', ''), 'Neighborhood', ''), 'Los Feliz,Los Feliz', 'Los Feliz'), 'Foothill Trails District', 'Foothills Trails District'), 'Glassel Park', 'Glassell Park'), 'Neighhborhood Council', ''), 'Neighborhood Development Council', '') AS council,
           file_name
      FROM council_documents_cleaned_inner_1_v;


-- View: council_documents_cleaned_outer_v
CREATE VIEW council_documents_cleaned_outer_v AS
    SELECT action_year,
           action_date,
           trim(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(council, 'Neughborhood Council', ''), '(1st Submittal)', ''), '(2nd Submittal)', ''), 'Hollwood Hills West', 'Hollywood Hills West'), 'Hollywood Hils West', 'Hollywood Hills West'), 'Mid City WEST', 'Mid City West'), 'Los Feliz, Los Feliz', 'Los Feliz'), 'PICO', 'Pico'), 'Neighborhood Coucnil', ''), 'Neigbhorhood Council', ''), 'Playa Del Rey', 'Playa'), 'Wilshire Center Koreatown', 'Wilshire Center-Koreatown'), 'the ', ''), 'Neighbrohood Council', ''), 'Mid Town', 'Mid-Town'), 'Westchester-Playa', 'Westchester/Playa'), 'Coucnil', ''), 'Community Impact Statement from by', ''), 'VIllage', 'Village'), 'Coun', ''), 'Neighborhoos cil', ''), 'United s', '') ) AS council,
           file_name
      FROM council_documents_cleaned_inner_2_v;


-- View: council_file_seconder_frequency
CREATE VIEW council_file_seconder_frequency AS
    SELECT second,
           MAX(frequency) AS frequency
      FROM (
               SELECT mover,
                      second,
                      count(cf_number) AS frequency
                 FROM council_file
                WHERE mover IS NOT NULL AND 
                      second IS NOT NULL AND 
                      CAST (strftime('%Y', date_received) AS INTEGER) > 2010
                GROUP BY mover,
                         second
           )
     GROUP BY second;


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
