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



