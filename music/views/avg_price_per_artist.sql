CREATE VIEW avg_price_per_artist AS
SELECT
    ar.name,
    COALESCE( ROUND(avg(t.unit_price), 2)::text, 'not enogu data') as avg_price_per_track
FROM artist ar
left join album a on ar.artist_id = a.artist_id
left join track t on a.album_id = t.album_id
group by ar.name