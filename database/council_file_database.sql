--
-- This script creates the tables used in the extraction of data
-- from the Los Angeles City Clerk's Council File
-- Management System (CFMS).  It will create the tables in an
-- already created database.  To create the database, see
-- https://www.sqlite.org/quickstart.html
--
-- Text encoding used: UTF-8
--

PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: meta
DROP TABLE IF EXISTS meta;

CREATE TABLE meta (
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
    reward_expire_date  TEXT (20) 
);


-- Table: vote_results
DROP TABLE IF EXISTS vote_results;

CREATE TABLE vote_results (
    cf_number        STRING (10) NOT NULL,
    council_district INT         NOT NULL,
    council_member   TEXT (40),
    vote             TEXT (10),
    PRIMARY KEY (
        cf_number,
        council_district
    )
);


-- Table: votes
DROP TABLE IF EXISTS votes;

CREATE TABLE votes (
    cf_number    STRING (10) PRIMARY KEY
                             UNIQUE,
    meeting_date TEXT (10),
    meeting_type TEXT (20),
    vote_action  TEXT (20) 
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
