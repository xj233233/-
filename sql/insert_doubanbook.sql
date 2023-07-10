replace into book_country_num
  select
  country, count(*) as num
  from books
  group by country;

replace into book_publisher_num
  select
  publisher, count(*) as num
  from books
  group by publisher;

replace into book_presstime_num
  select
  press_time, count(*) as num
  from books
  group by press_time;


replace into book_score_num
  select
  score, count(*) as num
  from books
  group by score;

replace into book_people_title
  select people,title
  from books
  order by convert(people,unsigned) desc
  limit 10;