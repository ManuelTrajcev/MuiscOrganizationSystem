CREATE VIEW rank_list_artists AS
SELECT ar.name,
       count(il.invoice_line_id) AS num_invoices,
       COALESCE(SUM(i.total), 0) AS money_earned
FROM artist ar
         LEFT JOIN album al ON ar.artist_id = al.album_id
         LEFT JOIN track tr ON al.album_id = tr.album_id
         LEFT JOIN invoice_line il ON tr.track_id = il.track_id
         LEFT JOIN invoice i on il.invoice_id = i.invoice_id
GROUP BY ar.name
ORDER BY money_earned DESC;
