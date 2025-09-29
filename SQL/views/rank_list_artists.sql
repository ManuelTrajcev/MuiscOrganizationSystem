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
