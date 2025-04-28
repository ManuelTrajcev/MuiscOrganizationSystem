CREATE VIEW rank_list_artists AS
    SELECT
            (ar.name),
            count(il.invoice_line_id)
as num_invoices
    FROM artist ar
    left join album al on ar.artist_id = al.album_id
    left join track tr on al.album_id = tr.album_id
    left join invoice_line il on tr.track_id = il.track_id
    group by ar.name
    order by num_invoices desc
