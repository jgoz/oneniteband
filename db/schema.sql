drop table if exists gig;

create table gig (
  id integer primary key autoincrement,
  date date not null,
  title varchar(50) not null,
  place varchar(50)
);

drop table if exists bio;

create table bio (
  slug varchar(20) primary key,
  type varchar(15) not null,
  name varchar(50) not null,
  content text not null,
  image varchar(255),
  timestamp datetime not null
);
