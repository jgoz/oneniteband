drop table if exists gig;

create table gig (
  id integer primary key autoincrement,
  date date not null,
  title varchar(50) not null,
  place varchar(50)
);

drop table if exists bio; -- renamed to content
drop table if exists content;

create table content (
  slug varchar(20) primary key,
  content text,
  image varchar(255),
  timestamp datetime not null
);

drop table if exists admin;

create table admin (
  username varchar(30) primary key,
  hash varchar(255) not null
);
