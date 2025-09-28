DROP INDEX IF EXISTS idx_invoice_customer_id;
DROP INDEX IF EXISTS idx_invoice_line_invoice_id;
DROP INDEX IF EXISTS idx_track_genre_id;
DROP INDEX IF EXISTS idx_track_album_id;
DROP INDEX IF EXISTS idx_album_artist_id;
DROP INDEX IF EXISTS idx_genre_genreid_name;
DROP INDEX IF EXISTS idx_artist_artistid_name;
DROP INDEX IF EXISTS invoice_customer_id_idx;


DROP INDEX IF EXISTS album_pkey;
DROP INDEX IF EXISTS artist_pkey;
DROP INDEX IF EXISTS customer_pkey;
DROP INDEX IF EXISTS employee_pkey;
DROP INDEX IF EXISTS genre_pkey;
DROP INDEX IF EXISTS invoice_pkey;
DROP INDEX IF EXISTS invoice_line_pkey;
DROP INDEX IF EXISTS media_type_pkey;
DROP INDEX IF EXISTS playlist_pkey;
DROP INDEX IF EXISTS track_pkey;
DROP INDEX IF EXISTS playlist_track_pkey;
DROP INDEX IF EXISTS price_pkey;
DROP INDEX IF EXISTS contact_pkey;
DROP INDEX IF EXISTS playlist_track_playlist_id_idx;
DROP INDEX IF EXISTS invoice_line_track_id_idx;
DROP INDEX IF EXISTS album_artist_id_idx;
DROP INDEX IF EXISTS customer_support_rep_id_idx;
DROP INDEX IF EXISTS employee_reports_to_idx;
DROP INDEX IF EXISTS invoice_line_invoice_id_idx;
DROP INDEX IF EXISTS invoice_line_track_id_idx;
DROP INDEX IF EXISTS playlist_track_track_id_idx;
DROP INDEX IF EXISTS playlist_track_playlist_id_idx;
DROP INDEX IF EXISTS track_album_id_idx;
DROP INDEX IF EXISTS track_genre_id_idx;
DROP INDEX IF EXISTS track_media_type_id_idx;
DROP INDEX IF EXISTS track_media_type_id_idx;

SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'invoice';

SELECT 'DROP INDEX IF EXISTS ' || indexname || ';'
FROM pg_indexes
WHERE tablename = 'invoice'
  AND indexname NOT IN (
      SELECT conname
      FROM pg_constraint
      WHERE conrelid = 'invoice'::regclass
  );

SELECT  indexname
FROM pg_indexes
WHERE tablename IN (
    'album',
    'artist',
    'customer',
    'employee',
    'genre',
    'invoice',
    'invoice_line',
    'media_type',
    'playlist',
    'playlist_track',
    'track',
    'price',
    'contact',
    'addressinfo'
);

-- Customer → Invoice (filter + join)
CREATE INDEX idx_invoice_customer_id
    ON invoice(customer_id);

-- Invoice → InvoiceLine (join)
CREATE INDEX idx_invoice_line_invoice_id
    ON invoice_line(invoice_id);

-- InvoiceLine → Track (join)
CREATE INDEX idx_invoice_line_track_id
    ON invoice_line(track_id);

-- Track → Genre (join)
CREATE INDEX idx_track_genre_id
    ON track(genre_id);

-- Track → Album (join)
CREATE INDEX idx_track_album_id
    ON track(album_id);

-- Album → Artist (join)
CREATE INDEX idx_album_artist_id
    ON album(artist_id);