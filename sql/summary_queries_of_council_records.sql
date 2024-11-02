select json_object('mover', mover_name, 'children', 
  (select json_group_array(json_object('name', second, 'weight', weight))
     from (
       select cf.second, substr(count(*)/(select strftime('%Y', julianday('now')) - strftime('%Y', julianday(start_date)) * 1.0 from council_district_member where mover_name = cf.mover), 1, 6) as weight
       from council_file cf
       where cf.mover = cdm.mover_name
       and cast(substr(cf.date_received, 1, 4) as integer) > 2010
       and second in (select mover_name from council_district_member where end_date is null)
       group by cf.second
     )
   )
) as mover_seconder
from council_district_member as cdm where end_date is null
order by mover_name;

select json_object('name', mover_name, 'children', (select json_group_array(json_object('name', second, 'weight', weight)) from ( select cf.second, count(*) as weight from council_file cf where cf.mover = cdm.mover_name and cast(substr(cf.date_received, 1, 4) as integer) > 2010 and second in (select mover_name from council_district_member where end_date is null) group by cf.second )))from council_district_member as cdm where end_date is null order by mover_name;

select json_group_array(json_object('name', second, 'weight', weight))
        from (select cf.second, count(*)/(select strftime('%Y', julianday('now')) - strftime('%Y', julianday(start_date)) * 1.0 from council_district_member where mover_name = cf.mover) as weight
         from council_file cf
         where cf.mover = 'BOB BLUMENFIELD'
         and cast(substr(cf.date_received, 1, 4) as integer) > 2010
         and second in (select mover_name from council_district_member where end_date is null)
         group by cf.second
         )
    group by second ;

select second, count(*) as weight from council_file cf
         where cf.mover = 'BOB BLUMENFIELD'
         and cast(substr(cf.date_received, 1, 4) as integer) > 2010
         and second in (select mover_name from council_district_member where end_date is null)
    group by cf.second ;
    
select strftime('%Y', julianday('now'));

select mover_name, start_date, strftime('%Y', julianday('now')) - strftime('%Y', julianday(start_date)) 
from council_district_member;

SELECT *
FROM council_district_member
WHERE LENGTH(end_date) = 0
ORDER BY CAST(district_n AS INTEGER);

update council_district_member
set start_date = substr(start_date, length(start_date) - 3, 4) || '-' 
   || replace(replace(start_date, '/' || substr(start_date, length(start_date) - 3, 4), ''), '/', '-');

select start_date, substr(start_date, length(start_date) - 3, 4) || '-' 
   || replace(replace(start_date, '/' || substr(start_date, length(start_date) - 3, 4), ''), '/', '-')  from council_district_member;

select start_date from    council_district_member where start_date like '%-1';
update council_district_member
set start_date = replace(start_date, '-9', '-09') where start_date like '%-9';


select distinct cd.cf_number from council_documents cd
  left outer join council_file cf on cd.cf_number = cf.cf_number
where cf.cf_number IS NULL;

select * from council_documents
where cf_number like '%0000';

-- Moves by topic
select SUBSTR(cf.date_received, 1, 4) AS Year, cf.mover, lt.topic_label, count(*) AS Frequency
from legislative_topic AS lt
  JOIN council_file_legislative_topic AS cflt ON lt.topic_id = cflt.topic_id
  JOIN council_file AS cf ON cflt.cf_number = cf.cf_number
WHERE CAST(Year AS INTEGER) < 2022
GROUP BY Year, mover, lt.topic_label
ORDER BY Year, mover, Frequency;

select vote_action, count(*) as frequency
from votes 
group by vote_action
order by frequency desc;

-- Voting activity
select substr(cf.date_received, 1, 4) as Year, cf.mover, vr.council_member, vr.vote, count(*)
from council_vote_result vr
join council_file cf on vr.cf_number = cf.cf_number
where cf.mover is not null and cf.date_received is not null
group by Year, cf.mover, vr.council_member, vr.vote;


select * from council_document 
where title like '%impact%'
limit 100;

-- looking at community impact statements as a measure of NC engagement
select action_year, council, file_name
from council_documents_cleaned_outer_v
where length(council) > 0 and council != 'by Mid City West';

-- looking at community impact statements as a measure of NC engagement- just the summary
select council, count(*) as Frequency
from council_documents_cleaned_outer_v
where length(council) > 0 and council != 'by Mid City West'
group by council
order by Frequency DESC;

select distinct council 
from council_documents_cleaned_outer_v
where length(council) > 0
order by council;

select * from council_documents 
  where title like '%Voices%' and (title like 'Community Impact Statement from%' or title like 'Community Impact Statement submitted by%');

-- summarize the council files with the greatest number of NC CIS' submitted
select cf.cf_number, cf.title, count(*) from council_document cd
  join council_file cf on cd.cf_number = cf.cf_number
where file_name like '%cis%'
group by cf.title
order by count(*) desc;

-- summarize the council files with the greatest number of public comments submitted - issue here is that multiple comments get attached per day submitted
select cf.cf_number, cf.title, count(*) 
from council_document cd
  join council_file cf on cd.cf_number = cf.cf_number
where LOWER(cd.title) like '%communication from public%' OR LOWER(cd.title) like '%communication(s) from public%'
group by cf.title
order by count(*) desc;

SELECT *
FROM council_document
ORDER BY cf_number DESC;


select * from council_file where lower(mover) like '%bonin%';

-- Analyzing vote activity
-- Here we are creating a directed graph
SELECT cf.mover as 'from', cf.second as 'to', count(*) as weight 
from council_file cf
join council_district_member cm on cf.mover = cm.mover_name
where LENGTH(cm.end_date) = 0 and mover is not null and second is not null 
 and cast(substr(date_received, 1, 4) as integer) > 2010
 and second in (select mover_name from council_district_member where LENGTH(end_date) = 0)
group by mover, second order by mover;

-- summarize active council member total activity by tenure
SELECT ti.name_last, ti.name_first,ti.start_date, ti.tenure, m.mover_count, SUBSTR(CAST(m.mover_count AS FLOAT) / CAST(ti.tenure AS FLOAT), 1, 6) AS adjusted_mover_count 
FROM (
  SELECT name_last, name_first, mover_name, start_date, CASE WHEN LENGTH(end_date) > 0 THEN
          CASE WHEN CAST(SUBSTR(start_date, LENGTH(start_date) - 1) AS INTEGER) > 50 THEN 
          strftime("%Y", date()) - CAST("19" || SUBSTR(start_date, LENGTH(start_date) - 1) AS INTEGER) ELSE
          strftime("%Y", date()) - CAST("20" || SUBSTR(start_date, LENGTH(start_date) - 1) AS INTEGER)  END
      ELSE
          CASE WHEN CAST(SUBSTR(start_date, LENGTH(start_date) - 1) AS INTEGER) > 50 THEN 
          strftime("%Y", date()) - CAST("19" || SUBSTR(start_date, LENGTH(start_date) - 1) AS INTEGER) ELSE
          strftime("%Y", date()) - CAST("20" || SUBSTR(start_date, LENGTH(start_date) - 1) AS INTEGER)  END
      END 
AS tenure
FROM council_district_member
WHERE LENGTH(end_date) = 0) as ti JOIN (
  SELECT mover, count(*) as mover_count
  FROM council_file 
  WHERE LENGTH(mover) > 0
  GROUP BY mover) as m on ti.mover_name = m.mover;


SELECT cf.mover as 'from', cf.second as 'to', count(*) as weight 
from council_file cf
join council_district_member cm on cf.mover = cm.mover_name
where LENGTH(cm.end_date) = 0 and mover is not null and second is not null 
 and cast(substr(date_received, 1, 4) as integer) > 2010
 and second in (select mover_name from council_district_member where LENGTH(end_date) = 0)
group by mover, second order by mover;

/* API Query to get json summary of all counfil files and their mover-second relationships */
select json_group_array(
select cf.mover as mover, cf.second as second, count(*) as weight
        from council_file cf
    join council_district_member cm on cf.mover = cm.mover_name
    where cm.end_date is null and mover is not null and second is not null 
     and cast(substr(date_received, 1, 4) as integer) > 2010
     and second in (select mover_name from council_district_member where end_date is null)
    group by mover, second order by mover
    
select json_group_object(mover, x) as name
from (
  select mover,
  json_object('children', json_array(json_object('name', second), json_object('weight', weight))) as x
  from (select cf.mover as mover, cf.second as second, count(*) as weight
        from council_file cf
    join council_district_member cm on cf.mover = cm.mover_name
    where cm.end_date is null and mover is not null and second is not null 
     and cast(substr(date_received, 1, 4) as integer) > 2010
     and second in (select mover_name from council_district_member where end_date is null)
    group by mover, second order by mover
   )) group by mover;
   
select distinct cf.mover 
from council_file cf
join council_district_member cm on cf.mover = cm.mover_name
where cm.end_Date is null;

select title, count(*) as Freq 
from council_document
group by title
order by Freq desc;

select *
from council_file
where cf_number = '20-0001'

select * from council_file
where cf_number = '21-1358'

select * from council_action where cf_number = '21-1358'

select * from council_file where title like '%ballona%' 
order by cast(substr(date_received, 1, 4) as integer) DESC

select * from council_file where cf_number = '22-0151'
select * from council_document where cf_number = '22-0151'

select cf.cf_number, cf.date_received, cd.file_name
from council_document cd
   join council_file cf on cd.cf_number = cd.cf_number
where cd.title = 'Motion'

   and SUBSTRING(action_date, 9, 2) != SUBSTRING(file_name, 1, 2)
select SUBSTRING(action_date, 9, 2), SUBSTRING(file_name, 1, 2) from council_document
SELECT * FROM council_file cf
WHERE cf_number NOT IN (
  SELECT cf_number FROM council_document WHERE title = 'Motion')
  
  left outer join council_document cd on cf.cf_number = cd.cf_number 
  where cd.cf_number is NULL
  
select * from council_file ORDER BY date_received DESC LIMiT 10;
select cf_number, mover, mover_comment from council_file where mover_comment is not null;
select cf_number, date_received, title, subject from council_file where subject  is not null order by date_received desc;

select council_district from council_file where council_district is not null;

select cf.*, lt.topic_id from council_file cf join council_file_legislative_topic lt on 
cf.cf_number = lt.cf_number where lt.topic_id in (3,4);

select vote_action, count(*)
from council_vote 
group by vote_action;

select vote, count(*)
from council_vote_result
group by vote

select * from council_documents_cleaned_outer_v

SELECT * FROM council_file_legislative_topic;

-- Relationship of mover to second - maybe to put in a sankey chart
SELECT mover as source, lt.topic_label as target, count(*) AS value
FROM council_file cf
JOIN council_district_member cd1 on cf.MOVER = cd1.mover_name and LENGTH(cd1.end_date) = 0
JOIN council_file_legislative_topic flt ON flt.cf_number = cf.cf_number
JOIN legislative_topic lt on flt.topic_id = lt.topic_id
GROUP BY  source, target;

-- Legislative topic review
SELECT lt.topic_label, dm.name_last, dm.name_first, dm.district_n, count(*) as Frequency
FROM legislative_topic lt JOIN council_file_legislative_topic flt on lt.topic_id = flt.topic_id
  JOIN council_file cf ON flt.cf_number = cf.cf_number
  JOIN council_district_member dm on cf.mover = dm.mover_name
  WHERE LENGTH(cf.mover) > 0 AND LENGTH(dm.end_date) = 0
  GROUP BY  lt.topic_label, dm.name_last, dm.name_first, dm.district_n;