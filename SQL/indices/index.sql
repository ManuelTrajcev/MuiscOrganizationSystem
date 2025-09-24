CREATE INDEX idx_invoice_customer_id
    ON invoice(customer_id);

CREATE INDEX idx_invoice_line_invoice_id
    ON invoice_line(invoice_id);

CREATE INDEX idx_track_genre_id
    ON track(genre_id);

CREATE INDEX idx_track_album_id
    ON track(album_id);

CREATE INDEX idx_album_artist_id
    ON album(artist_id);

CREATE INDEX idx_genre_genreid_name
    ON genre(genre_id, name);

CREATE INDEX idx_artist_artistid_name
    ON artist(artist_id, name);
