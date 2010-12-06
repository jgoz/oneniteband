-- Gigs
delete from gig;

insert into gig (date, title, place) values (
  '2010-11-20',
  'Firefighter''s Ball',
  'Nanton, AB'
);

insert into gig (date, title) values (
  '2010-12-03',
  'Nanton Queen''s Ball'
);

insert into gig (date, title, place) values (
  '2009-12-07',
  'Gig of DEATH',
  'Nanton, AB'
);

-- Content
delete from content;

insert into content (slug, content, image, timestamp) values (
  'band_bio',
  '<p><strong>One Nite Band</strong> has been the life of the party at all kinds of weddings and events in the Calgary area since 2002. Our vocalists trained with the Youth Singers of Calgary. Our rhythm and horn players have been playing jazz, rock and pop for more years than we''d care to mention. Some of us have even played internationally &mdash; in Cuba &mdash; during a hurricane.</p>',
  null,
  'now'
);
