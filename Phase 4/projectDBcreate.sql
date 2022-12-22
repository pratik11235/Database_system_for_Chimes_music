create table fall22_s004_10_songs(
  song_id number(10),
  -- song name can not be null
  song_name varchar(50) not null,
  -- genre can have only 4 values
  genre varchar(10) check (genre in ('Rap', 'Hiphop', 'Jazz', 'RnB')),
  -- region can have only 3 values
  region number(1) check (region in (1,2,3)),
  -- release date in format mm-dd-yyyy
  release_date char(10) check (release_date like '%-%-%'),
  primary key (song_id)
);

create table fall22_s004_10_avail_songs(
  song_id number(10),
  avail_song_id number(10) not null,
  purchase_price number(10) not null,
  rent_price number(10) not null,
  song_duration number(10), -- in seconds
  primary key (song_id),
  foreign key (song_id) 
  references fall22_s004_10_songs(song_id) 
  on delete cascade,
  unique (avail_song_id)
);

create table fall22_s004_10_unavail_songs(
  song_id number(10),
  unavail_song_id number(10) not null,
  primary key (song_id),
  foreign key (song_id) 
  references fall22_s004_10_songs(song_id) 
  on delete cascade,
  unique (unavail_song_id)
);

create table fall22_s004_10_person(
  pid number(10),
  fname varchar(20) not null,
  mname varchar(20),
  lname varchar(20) not null,
  gender char check(gender = 'f' or gender = 'm'),
  dob char(10) check (dob like '%-%-%'),
  primary key (pid),
  unique (fname, mname, lname)
);

create table fall22_s004_10_person_phone(
  pid number(10),
  phone_no number(10),
  primary key (pid, phone_no),
  foreign key (pid)
  references fall22_s004_10_person(pid)
  on delete cascade
);

create table fall22_s004_10_person_email(
  pid number(10),
  email varchar(40),
  primary key (pid, email),
  foreign key (pid)
  references fall22_s004_10_person(pid)
  on delete cascade
);

create table fall22_s004_10_customer(
  pid number(10),
  cust_id number(10) not null,
  username varchar(20) not null, 
  password varchar(20) not null,
  cust_region number(1) check (cust_region in (1,2,3)),
  primary key (pid),
  foreign key (pid)
  references fall22_s004_10_person(pid)
  on delete cascade,
  unique (cust_id),
  unique (username)
);

create table fall22_s004_10_customer_genre_pref(
  cust_id number(10),
  genre_pref varchar(10) check (genre_pref in ('Rap', 'Hiphop', 'Jazz', 'RnB')),
  primary key (cust_id, genre_pref),
  foreign key (cust_id)
  references fall22_s004_10_customer(cust_id)
  on delete cascade
);

create table fall22_s004_10_producers(
  pid number(10),
  producer_id number(10) not null,
  primary key (pid),
  foreign key (pid)
  references fall22_s004_10_person(pid)
  on delete cascade,
  unique (producer_id)
);

create table fall22_s004_10_artist(
  pid number(10),
  artist_id number(10) not null,
  artist_region number(1) check (artist_region in (1,2,3)),
  primary key (pid),
  foreign key (pid)
  references fall22_s004_10_person(pid)
  on delete cascade,
  unique (artist_id)
);

create table fall22_s004_10_singer(
  artist_id number(10),
  singer_id number(10) not null,
  primary key (artist_id),
  foreign key (artist_id)
  references fall22_s004_10_artist(artist_id)
  on delete cascade,
  unique (singer_id)
);

create table fall22_s004_10_composer(
  artist_id number(10),
  composer_id number(10) not null,
  primary key (artist_id),
  foreign key (artist_id)
  references fall22_s004_10_artist(artist_id)
  on delete cascade,
  unique (composer_id)
);

create table fall22_s004_10_buys_rents(
  avail_song_id number(10),
  cust_id number(10),
  trans_id number(12) not null,
  -- trans_type indicates whether transaction is Rent or Buy
  trans_type char(1) check(trans_type = 'R' or trans_type = 'B'),
  pay_mode varchar(5) check(pay_mode in ('credt', 'debit', 'bankt')),
  trans_date char(10) check (trans_date like '%-%-%'),
  trans_time char(8) check(trans_time like '%:%:%'),
  bank_name varchar(30),
  duration number(10), -- in months
  primary key (avail_song_id, cust_id),
  foreign key (avail_song_id)
  references fall22_s004_10_avail_songs(avail_song_id)
  on delete cascade,
  foreign key (cust_id)
  references fall22_s004_10_customer(cust_id)
  on delete cascade,
  unique (trans_id)
);

create table fall22_s004_10_likes(
  avail_song_id number(10),
  cust_id number(10),
  primary key (avail_song_id, cust_id),
  foreign key (avail_song_id)
  references fall22_s004_10_avail_songs(avail_song_id)
  on delete cascade,
  foreign key (cust_id)
  references fall22_s004_10_customer(cust_id)
  on delete cascade
);

create table fall22_s004_10_requests(
  unavail_song_id number(10),
  cust_id number(10),
  request_id number(12),
  req_date char(10) check (req_date like '%-%-%'),
  req_time char(8) check(req_time like '%:%:%'),
  primary key (unavail_song_id, cust_id),
  foreign key (unavail_song_id)
  references fall22_s004_10_unavail_songs(unavail_song_id)
  on delete cascade,
  foreign key (cust_id)
  references fall22_s004_10_customer(cust_id)
  on delete cascade,
  unique (request_id)
);

create table fall22_s004_10_produces(
  song_id number(10),
  producer_id number(10),
  --prod_date char(10) check (prod_date like '%-%-%'),
  primary key (song_id, producer_id),
  foreign key (song_id) 
  references fall22_s004_10_songs(song_id) 
  on delete cascade,
  foreign key (producer_id)
  references fall22_s004_10_producers(producer_id)
  on delete cascade
);

create table fall22_s004_10_follows(
  cust_id number(10),
  artist_id number(10),
  primary key (cust_id, artist_id),
  foreign key (artist_id)
  references fall22_s004_10_artist(artist_id)
  on delete cascade,
  foreign key (cust_id)
  references fall22_s004_10_customer(cust_id)
  on delete cascade
);

create table fall22_s004_10_sings(
  song_id number(10),
  singer_id number(10),
  primary key (song_id, singer_id),
  foreign key (song_id) 
  references fall22_s004_10_songs(song_id) 
  on delete cascade,
  foreign key (singer_id) 
  references fall22_s004_10_singer(singer_id) 
  on delete cascade
);

create table fall22_s004_10_composes(
  song_id number(10),
  composer_id number(10),
  primary key (song_id, composer_id),
  foreign key (song_id) 
  references fall22_s004_10_songs(song_id) 
  on delete cascade,
  foreign key (composer_id) 
  references fall22_s004_10_composer(composer_id) 
  on delete cascade
);






