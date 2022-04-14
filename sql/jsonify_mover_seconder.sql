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
order by mover_name

select json_object('name', mover_name, 'children', (select json_group_array(json_object('name', second, 'weight', weight)) from ( select cf.second, count(*) as weight from council_file cf where cf.mover = cdm.mover_name and cast(substr(cf.date_received, 1, 4) as integer) > 2010 and second in (select mover_name from council_district_member where end_date is null) group by cf.second )))from council_district_member as cdm where end_date is null order by mover_name

select json_group_array(json_object('name', second, 'weight', weight))
        from (select cf.second, count(*)/(select strftime('%Y', julianday('now')) - strftime('%Y', julianday(start_date)) * 1.0 from council_district_member where mover_name = cf.mover) as weight
         from council_file cf
         where cf.mover = 'BOB BLUMENFIELD'
         and cast(substr(cf.date_received, 1, 4) as integer) > 2010
         and second in (select mover_name from council_district_member where end_date is null)
         group by cf.second
         )
    group by second 

select second, count(*) as weight from council_file cf
         where cf.mover = 'BOB BLUMENFIELD'
         and cast(substr(cf.date_received, 1, 4) as integer) > 2010
         and second in (select mover_name from council_district_member where end_date is null)
    group by cf.second 
    
select strftime('%Y', julianday('now'))
select mover_name, start_date, strftime('%Y', julianday('now')) - strftime('%Y', julianday(start_date)) from council_district_member

update council_district_member
set start_date = substr(start_date, length(start_date) - 3, 4) || '-' 
   || replace(replace(start_date, '/' || substr(start_date, length(start_date) - 3, 4), ''), '/', '-')

select start_date, substr(start_date, length(start_date) - 3, 4) || '-' 
   || replace(replace(start_date, '/' || substr(start_date, length(start_date) - 3, 4), ''), '/', '-')  from council_district_member

select start_date from    council_district_member where start_date like '%-1'
update council_district_member
set start_date = replace(start_date, '-9', '-09') where start_date like '%-9'
