delete from fall22_s004_10_songs where song_id in (1,2,3,4,5);
delete from fall22_s004_10_producers where producer_id in (50001, 50002, 50003, 50004, 50005);
delete from fall22_s004_10_singer where singer_id in (70001, 70002, 70003, 70004, 70005);
delete from fall22_s004_10_composer where composer_id in (900121, 900122, 900123, 900124, 900125);

update fall22_s004_10_person set fname = 'Pratik Antoni', lname = 'Patekar' where pid = 2018;
update fall22_s004_10_person set fname = 'Sanket', lname = 'More' where pid = 2011;
update fall22_s004_10_person set fname = 'Keyur', lname = 'Mushrif' where pid = 2037;
update fall22_s004_10_person set fname = 'Raju', lname = 'Oberoi' where pid = 2006;
