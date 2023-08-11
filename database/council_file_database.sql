
CREATE TABLE council_action (
    cf_number   STRING (10) REFERENCES council_file (cf_number),
    action_date TEXT (10),
    description TEXT
);
CREATE TABLE council_distance_matrix (
    council_id1 INTEGER,
    council_id2 INTEGER,
    distance    INTEGER
);
CREATE TABLE council_district (
    district_n INTEGER PRIMARY KEY,
    district   TEXT
);
CREATE TABLE council_district_member (
    district_n INTEGER REFERENCES council_district (district_n),
    name_last  TEXT,
    name_first TEXT,
    start_date DATE,
    end_date   DATE,
    mover_name TEXT
);
CREATE TABLE council_document (
    cf_number   TEXT      REFERENCES council_file (cf_number),
    action_date TEXT (10),
    title       TEXT,
    file_name   TEXT
);
CREATE TABLE council_file (
    cf_number           STRING (10) PRIMARY KEY
                                    UNIQUE
                                    NOT NULL,
    council_district    INT,
    direct_to_council   TEXT (1),
    date_expiration     TEXT (10),
    date_last_changed   TEXT (10),
    date_received       TEXT (10),
    initiated_by        TEXT (40),
    mover               TEXT (40),
    mover_comment       TEXT (255),
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
CREATE TABLE council_file_legislative_topic (
    cf_number STRING (10) REFERENCES council_file (cf_number),
    topic_id  INTEGER     REFERENCES legislative_topic (topic_id) 
);
CREATE TABLE council_vote (
    cf_number    STRING (10) PRIMARY KEY
                             UNIQUE
                             REFERENCES council_file (cf_number),
    meeting_date TEXT (10),
    meeting_type TEXT (20),
    vote_action  TEXT (20) 
);
CREATE TABLE council_vote_result (
    cf_number        STRING (10) NOT NULL,
    council_district INT         NOT NULL,
    council_member   TEXT (40),
    vote             TEXT (10),
    PRIMARY KEY (
        cf_number,
        council_district
    )
);
CREATE TABLE legislative_topic (
    topic_id       INTEGER PRIMARY KEY,
    topic_label    TEXT,
    topic_keywords TEXT
);
