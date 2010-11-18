drop table if exists content;

create table content (
  key text primary key,
  page text not null,
  text text not null
);
