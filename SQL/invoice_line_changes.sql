ALTER TABLE invoice_line
    DROP CONSTRAINT invoice_line_pkey;

DROP view rank_list_artists;
CREATE VIEW rank_list_artists AS
SELECT
    ar.name,
    COUNT(il.invoice_id) AS num_invoices,
    COALESCE(SUM(i.total), 0) AS money_earned
FROM artist ar
LEFT JOIN album al ON ar.artist_id = al.artist_id
LEFT JOIN track tr ON al.album_id = tr.album_id
LEFT JOIN invoice_line il ON tr.track_id = il.track_id
LEFT JOIN invoice i ON il.invoice_id = i.invoice_id
WHERE ar.deleted_at IS NULL
GROUP BY ar.name
ORDER BY money_earned DESC;


ALTER TABLE invoice_line
    DROP COLUMN invoice_line_id;


DROP TRIGGER IF EXISTS trg_soft_delete_invoice_line ON invoice_line;
DROP FUNCTION IF EXISTS soft_delete_invoice_line();

CREATE FUNCTION soft_delete_invoice_line()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE invoice_line
    SET deleted_at = NOW()
    WHERE invoice_id = OLD.invoice_id
      AND track_id = OLD.track_id;
    RETURN NULL;
END;
$$;

CREATE TRIGGER trg_soft_delete_invoice_line
AFTER DELETE ON invoice_line
FOR EACH ROW
EXECUTE FUNCTION soft_delete_invoice_line();


delete
from invoice_line
where invoice_id = 2 and track_id=6;


ALTER TABLE invoice_line
    ADD CONSTRAINT invoice_line_pkey PRIMARY KEY (invoice_id, track_id);