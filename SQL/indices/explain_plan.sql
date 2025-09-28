EXPLAIN (ANALYZE, BUFFERS)
WITH PlayCounts AS (
    SELECT
        g.genre_id,
        g.name AS genre_name,
        ar.name AS artist_name,
        COUNT(*) AS play_count
    FROM customer c
    JOIN invoice i ON c.customer_id = i.customer_id
    JOIN invoice_line il ON i.invoice_id = il.invoice_id
    JOIN track tr ON il.track_id = tr.track_id
    JOIN genre g ON tr.genre_id = g.genre_id
    JOIN album a ON tr.album_id = a.album_id
    JOIN artist ar ON a.artist_id = ar.artist_id
    WHERE c.customer_id = 5   -- example input
    GROUP BY g.genre_id, g.name, ar.name
),
MaxPlayCounts AS (
    SELECT genre_id, MAX(play_count) AS max_count
    FROM PlayCounts
    GROUP BY genre_id
)
SELECT pc.genre_name, pc.artist_name, pc.play_count
FROM PlayCounts pc
JOIN MaxPlayCounts mpc
  ON pc.genre_id = mpc.genre_id AND pc.play_count = mpc.max_count;