--
-- File generated with SQLiteStudio v3.3.3 on Sat Apr 9 07:24:26 2022
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: council_action
CREATE TABLE council_action (cf_number STRING (10), action_date TEXT (10), description TEXT);

-- Table: council_distance_matrix
CREATE TABLE "council_distance_matrix" (
	"council_id1"	INTEGER,
	"council_id2"	INTEGER,
	"distance"	INTEGER
);

-- Table: council_district
CREATE TABLE council_district (district_n INTEGER PRIMARY KEY, district TEXT);

-- Table: council_district_member
CREATE TABLE council_district_member (district_n INTEGER, name_last TEXT, name_first TEXT, start_date DATE, end_date DATE, mover_name TEXT);

-- Table: council_document
CREATE TABLE council_document (cf_number TEXT, action_date TEXT (10), title TEXT, file_name TEXT);

-- Table: council_file
CREATE TABLE council_file (cf_number STRING (10) PRIMARY KEY UNIQUE NOT NULL, council_district INT, direct_to_council TEXT (1), date_expiration TEXT (10), date_last_changed TEXT (10), date_received TEXT (10), initiated_by TEXT (40), mover TEXT (40), mover_comment TEXT (255), pending_committee TEXT (100), reference_recs TEXT (400), second TEXT (40), title TEXT (256), reward_amount TEXT (20), reward_duration TEXT (20), reward_publish_date TEXT (20), reward_expire_date TEXT (20), subject TEXT (1000));

-- Table: council_file_legislative_topic
CREATE TABLE council_file_legislative_topic (cf_number STRING (10), topic_id INTEGER);

-- Table: legislative_topic
CREATE TABLE legislative_topic (topic_id INTEGER PRIMARY KEY, topic_label TEXT, topic_keywords TEXT);

-- Table: vote_results
CREATE TABLE vote_results (
    cf_number        STRING (10) NOT NULL,
    council_district INT NOT NULL,
    council_member   TEXT (40),
    vote             TEXT (10) ,
     PRIMARY KEY (cf_number, council_district)
);

-- Table: votes
CREATE TABLE votes (cf_number STRING (10) PRIMARY KEY UNIQUE, meeting_date TEXT (10), meeting_type TEXT (20), vote_action TEXT (20));

-- View: council_documents_cleaned_inner_v
CREATE VIEW council_documents_cleaned_inner_v AS SELECT substr(action_date, 7, 10) AS action_year, action_date, "replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"("replace"(title, 'Voices Neighborhood Council', 'Voices of 90037 Neighborhood Council'), 'Community Impact Statement from', ''), 'Community Impact Statement submitted by ', ''), ' Community Council', ''), ' Neighborhood Council', ''), ' (e)', ''), 'Bel-Air Beverly', 'Bel Air-Beverly'), 'Community Impact Statement submitted by', ''), 'Neighbhood Council', ''), ' ofs', ''), '- 2nd Submission', ''), 'Neightborhood Council', ''), 'Neighhborhood Council', ''), 'Neighborhood Development Council', ''), 'Community Impact Statement Submitted by ', ''), 'Historic Cultural North,Historic Cultural North', 'Historic Cultural North'), 'neighborhood Council', ''), 'NC', ''), 'Neighborhood Council of', ''), 'Neighborhood Council', ''), 'Neighbhorhood Council', ''), 'United Neighborhoods of the ', ''), 'NDC', ''), '(EH)', ''), 'Neighborhood', ''), 'Los Feliz,Los Feliz', 'Los Feliz'), 'Foothill Trails District', 'Foothills Trails District'), 'Glassel Park', 'Glassell Park') AS council, file_name FROM council_document WHERE title LIKE 'Community Impact Statement from%' or title LIKE 'Community Impact Statement submitted by%';

-- View: council_documents_cleaned_outer_v
CREATE VIEW council_documents_cleaned_outer_v AS select action_year, action_date, trim(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(council, 
       'Neughborhood Council', ''), '(1st Submittal)', ''), '(2nd Submittal)', ''),
       'Hollwood Hills West', 'Hollywood Hills West'), 'Hollywood Hils West', 'Hollywood Hills West'),
       'Mid City WEST', 'Mid City West'), 'Los Feliz, Los Feliz', 'Los Feliz'), 'PICO', 'Pico'),
       'Neighborhood Coucnil', ''), 'Neigbhorhood Council', ''), 'Playa Del Rey', 'Playa'),
       'Wilshire Center Koreatown', 'Wilshire Center-Koreatown'), 'the ', ''), 'Neighbrohood Council', ''),
       'Mid Town', 'Mid-Town'), 'Westchester-Playa', 'Westchester/Playa'), 'Coucnil', ''),
       'Community Impact Statement from by', ''), 'VIllage', 'Village'), 'Coun', ''),
       'Neighborhoos cil', ''), 'United s', '')) as council, file_name
from council_documents_cleaned_inner_v;

-- View: council_file_seconder_frequency
CREATE VIEW council_file_seconder_frequency AS SELECT second,
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
