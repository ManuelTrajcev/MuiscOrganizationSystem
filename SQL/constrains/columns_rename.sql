ALTER TABLE artist
RENAME COLUMN name TO artist_name;

ALTER TABLE track
RENAME COLUMN name TO track_name;

ALTER TABLE price
RENAME COLUMN date TO price_date;

ALTER TABLE media_type
RENAME COLUMN name TO media_type_name;

ALTER TABLE genre
RENAME COLUMN name TO genre_name;

ALTER TABLE album
RENAME COLUMN title TO album_title;

ALTER TABLE employee
RENAME COLUMN title TO employee_title;