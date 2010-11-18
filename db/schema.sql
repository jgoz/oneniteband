drop table if exists gig;

create table gig (
  id integer primary key autoincrement,
  date date not null,
  title varchar(50) not null,
  place varchar(50)
);
