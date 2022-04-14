-- insert into council_district (district_n, district) values (1, 'CD 1') 
insert into council_district (district_n, district) values (2, 'CD 2') 
insert into council_district (district_n, district) values (3, 'CD 3') 
insert into council_district (district_n, district) values (4, 'CD 4') 
insert into council_district (district_n, district) values (5, 'CD 5') 
insert into council_district (district_n, district) values (6, 'CD 6') 
insert into council_district (district_n, district) values (7, 'CD 7') 
insert into council_district (district_n, district) values (8, 'CD 8') 
insert into council_district (district_n, district) values (9, 'CD 9') 
insert into council_district (district_n, district) values (10, 'CD 10') 
insert into council_district (district_n, district) values (11, 'CD 11') 
insert into council_district (district_n, district) values (12, 'CD 12') 
insert into council_district (district_n, district) values (13, 'CD 13') 
insert into council_district (district_n, district) values (14, 'CD 14') 
insert into council_district (district_n, district) values (15, 'CD 15') 

insert into council_district_member (district_n, name_first, name_last, start_date, end_date) 
values (15, 'Rudy','Svorinich, Jr.', '7/1/1994', '7/1/2001')

 (1, 'Ed','Reyes', '7/1/2001', '7/1/2013'),
(1, 'Mike','Hernandez', '7/1/1991', '7/1/2001'),
(2, 'Wendy','Greuel', '7/1/2002', '7/1/2009'),
(2, 'Joel','Wachs', '7/1/1971', '7/1/2002'),
(3, 'Dennis','Zine', '7/1/2001', '7/1/2013'),
(4, 'Thomas','LaBonge', '11/1/2001', '7/1/2015'),
(4, 'David','Ryu', '7/1/2015', '12/14/2020'),
(5, 'Jack','Weiss', '7/1/2001', '7/1/2009'),
(6, 'Ruth','Galanter', '7/1/1987', '7/1/2003'),
(6, 'Tony','Cárdenas', '7/1/2003', '8/9/2013'),
(7, 'Alex','Padilla', '7/1/1999', '7/1/2007'),
(7, 'Richard','Alarcon', '7/1/2007', '7/1/2013'),
(7, 'Felipe','Fuentes', '7/1/2013', '9/11/2016'),
(8, 'Mark','Ridley-Thomas', '7/1/1991', '12/1/2002'),
(8, 'Bernard','Parks', '7/1/2003', '7/1/2015'),
(9, 'Jan','Perry', '7/1/2001', '7/1/2013'),
(10, 'Martin','Ludlow', '7/1/2003', '6/30/2005'),
(11, 'Cindy','Miscikowski', '7/1/1997', '7/1/2005'),
(11, 'Bill','Rosendahl', '7/1/2005', '7/1/2013'),
(12, 'Greg','Smith','7/1/2003', '7/1/2011'),
(12, 'Mitchell','Englander','7/1/2011', '12/31/2018'),
(12, 'Greg','Smith','1/15/2019', '8/23/2019'),
(13, 'Eric','Garcetti', '7/1/2001', '7/1/2013'),
(14, 'José','Huizar', '12/1/2005', '10/15/2020'),
(14, 'Antonio','Villaraigosa', '7/1/2003', '7/1/2005'),
(14, 'Nick','Pacheco', '7/1/1999', '7/1/2003'),
(15, 'Janice','Hahn', '7/1/2001', '7/12/2011');

select * from council_district_member

select replace(mover, ' ', '-') as mover, count(*) from council_file cf 
   left outer join council_district_member cdm on lower(cf.mover) = lower(mover_name)
   WHERE cdm.district_n IS NULL
   group by mover
   
update council_district_member
set mover_name = UPPER(name_first) || ' ' || UPPER(name_last)

SELECT * from council_document limit 1, 20
SELECT * from council_file_legislative_topic 

select SUBSTR(date_received, 1, 4) as Year, mover, count(*) as Frequency
from council_file
where mover is not null
group by Year, mover

select * from council_file
where DATE(date_received) > DATE('2020-04-12') AND DATE(date_received) < DATE('2020-05-02')