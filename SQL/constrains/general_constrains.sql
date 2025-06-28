-- Default Media Type Constrain
ALTER TABLE track
ALTER COLUMN media_type_id SET DEFAULT 1;

ALTER TABLE track
DROP CONSTRAINT IF EXISTS track_media_type_id_fkey;

ALTER TABLE track
ADD CONSTRAINT track_media_type_id_fkey
FOREIGN KEY (media_type_id) REFERENCES media_type(media_type_id)
ON DELETE SET DEFAULT;


SELECT setval(pg_get_serial_sequence('invoice_line', 'invoice_line_id'), (SELECT MAX(invoice_line_id) FROM invoice_line));

SELECT setval(pg_get_serial_sequence('playlist_track', 'id'), (SELECT MAX(id) FROM playlist_track));

SELECT setval(pg_get_serial_sequence('playlist', 'playlist_id'), (SELECT MAX(playlist_id) FROM playlist));

SELECT setval(pg_get_serial_sequence('artist', 'artist_id'), (SELECT MAX(artist_id) FROM artist));

SELECT setval(pg_get_serial_sequence('album', 'album_id'), (SELECT MAX(album_id) FROM album));

SELECT setval(pg_get_serial_sequence('track', 'track_id'), (SELECT MAX(track_id) FROM track));

SELECT setval(pg_get_serial_sequence('media_type', 'media_type_id'), (SELECT MAX(media_type_id) FROM media_type));

SELECT setval(pg_get_serial_sequence('genre', 'genre_id'), (SELECT MAX(genre_id) FROM genre));

SELECT setval(pg_get_serial_sequence('customer', 'customer_id'), (SELECT MAX(customer_id) FROM customer));

SELECT setval(pg_get_serial_sequence('employee', 'employee_id'), (SELECT MAX(employee_id) FROM employee));


