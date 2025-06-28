CREATE VIEW avg_price_per_artist AS
WITH latest_price AS (
    SELECT DISTINCT ON (track_id)
        track_id,
        value
    FROM price
    ORDER BY track_id, date DESC
)
SELECT
    ar.name,
    COALESCE(ROUND(AVG(lp.value), 2)::text, 'not enough data') AS avg_price_per_track
FROM artist ar
LEFT JOIN album a ON ar.artist_id = a.artist_id
LEFT JOIN track t ON a.album_id = t.album_id
LEFT JOIN latest_price lp ON t.track_id = lp.track_id
GROUP BY ar.name
ORDER BY ar.name;