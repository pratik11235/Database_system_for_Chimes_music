-- Query 1: Using aggregation function 'count'
-- Write a query to find the number of available and unavailable songs
select status, count(song_id) as song_count
from  
      (-- get the song ids of available songs and assign 'Available' as status  
      (select songs.song_id, 'Available' as status 
      from fall22_s004_10_avail_songs asongs, fall22_s004_10_songs songs
      where (songs.song_id = asongs.song_id))
      union
      (-- get the song ids of unavailable songs and assign 'Unavailable' as status
      select songs.song_id, 'Unavailable' as status
      from fall22_s004_10_unavail_songs uasongs, fall22_s004_10_songs songs
      where (songs.song_id = uasongs.song_id)))
-- group by on Status and get song_count
group by status
order by song_count
;

-- Query 2: Find top 2 regions in which max number of customers have purchased/ rented till date 
select customer.cust_region, count(customer.cust_id) as count_cust
from fall22_s004_10_buys_rents buys_rents, fall22_s004_10_customer customer
where buys_rents.cust_id = customer.cust_id
group by cust_region
order by count_cust desc
fetch first 2 rows only
;

-- Query 3: find the top 10 singer names with highest no. of likes for their songs
select person.fname as singer_fname, person.lname as singer_lname, songs.song_name, count(*) as likes_count
from fall22_s004_10_likes likes, fall22_s004_10_avail_songs asongs, fall22_s004_10_sings sings, fall22_s004_10_songs songs, 
      fall22_s004_10_artist artist, fall22_s004_10_singer singer, fall22_s004_10_person person
where likes.avail_song_id = asongs.avail_song_id and
      asongs.song_id = songs.song_id and
      songs.song_id = sings.song_id and
      sings.singer_id = singer.singer_id and
      singer.artist_id = artist.artist_id and 
      artist.pid = person.pid
group by person.fname, person.lname, sings.singer_id, songs.song_name
order by likes_count desc
fetch first 10 rows only
;

-- Query 4: Find top 5 songs with maximum number of requests
select song_name, count(request_id) as req_count
from fall22_s004_10_requests requests, fall22_s004_10_unavail_songs uasongs, fall22_s004_10_songs songs
where requests.unavail_song_id = uasongs.unavail_song_id and 
      uasongs.song_id = songs.song_id
group by song_name
order by req_count desc
fetch first 5 rows only
;

-- Query 5: Find age group of customers who have made less number of purchases compared to other age group
-- age group            1: <35, 2: >=35
-- in terms of years:   1: 2022 and 1987, 2: 1986 and lesser
select age_group, count(age_group) as count_songs
from
        (
        select customer.cust_id, substr(person.dob, 7, 4), (case when (substr(person.dob, 7, 4) < '2022' and substr(person.dob, 7, 4) >= '1987') then 1 else 2 end) age_group
        from fall22_s004_10_customer customer, fall22_s004_10_person person, fall22_s004_10_buys_rents buys_rents
        where buys_rents.cust_id = customer.cust_id and
              customer.pid = person.pid and 
              buys_rents.trans_type = 'B'
        group by customer.cust_id, person.dob
              )
group by age_group
order by count_songs
fetch first 1 rows only
;


-- Query 6: Using group by and aggregation function 'count'
-- Write a query to find the customer name and the number of songs who have purchased atleast 2 songs

-- get the name of customer/ person from person table
select pid, fname, lname, count(song_id) as song_count
from fall22_s004_10_songs songs, fall22_s004_10_person person
where (songs.song_id, person.pid) in (-- get pid of customers from customers table
                                      select song_id, pid
                                      from fall22_s004_10_avail_songs asong, fall22_s004_10_customer cust
                                      where (asong.avail_song_id, cust.cust_id) in (-- get pruchase song history from buys_rents table
                                                                                    select avail_song_id, cust_id 
                                                                                    from fall22_s004_10_buys_rents
                                                                                    -- 'B' indicates that song is pruchased and not rented
                                                                                    where trans_type = 'B')
                                                                                    )
group by pid, fname, lname
having count(song_id) >= 2
order by song_count desc
fetch first 10 rows only
;

-- Query 7: Using group by and aggregation function count
-- List the number of songs that each producers have produced with singers from region 1
select person.fname as prod_fname, person.lname as prod_lname, song_count
from fall22_s004_10_person person, (select pid, producers.producer_id, count(song_id) as song_count
                                    from fall22_s004_10_producers producers, fall22_s004_10_produces produces
                                    where producers.producer_id = produces.producer_id and 
                                          song_id in (select song_id
                                                      from fall22_s004_10_singer singer, fall22_s004_10_sings sings, fall22_s004_10_artist artist
                                                      where singer.singer_id = sings.singer_id and
                                                            artist.artist_id = singer.artist_id and
                                                            artist.artist_region = 1)
                                    group by pid, producers.producer_id) prod
where person.pid = prod.pid
order by song_count desc
;

-- Query 8: 
-- ROLLUP query to find the payment mode that has max count for
-- buy i.e. purchase transaction 'B' and for rent transaction 'R'
select trans_type, pay_mode, bank_name, count(trans_id)
from fall22_s004_10_buys_rents
group by rollup (trans_type, pay_mode, bank_name);
-- from results we can see that for buying songs customers prefer 
-- using debit card payment mode and 
-- for renting customers prefer using bank transfer mode

-- Query 9:
-- CUBE query to find the number of songs that each producer has produced
-- with each composer
select artist_id, producer.producer_id, count(composes.song_id) as song_count
from fall22_s004_10_composer composer, 
     fall22_s004_10_composes composes,
     fall22_s004_10_producers producer, 
     fall22_s004_10_produces produces
where produces.song_id = composes.song_id and
      produces.producer_id = producer.producer_id and
      composes.composer_id = composer.composer_id
group by cube (artist_id, producer.producer_id) 
order by song_count desc    
;
-- from results we can see that the artist with artist id 600149 has composed highest number of songs
-- and producer with producer id 50036 has produced highest number of songs
-- we can also conclude that the highest number of songs that any composer has composed with producer is 2
-- for example: artist id 600158 and producer id 50039 have produced 2 songs together.
-- similar comclusions can be made regarding the other composers/ artists


-- Query 10
-- using OVER
-- find the cumulative sum of revenue generated from 2010 to 2021
select year, year_revenue, sum(year_revenue) over (order by year rows between unbounded preceding and current row) as cum_revenue
from (
        select year, sum(price) as year_revenue
        from (
                select substr(trans_date, 7, 4) as year, 
                      (case when trans_type = 'B' then purchase_price else rent_price end) as price
                from fall22_s004_10_buys_rents buys_rents, fall22_s004_10_avail_songs asongs
                where buys_rents.avail_song_id = asongs.avail_song_id
                )
        where year between '2010' and '2021'
        group by year
        order by year
        )
;









