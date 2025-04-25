CREATE VIEW track_count_per_genre AS
SELECT  g.name as Genre, count(t.track_id) as num_tracks
FROM genre g
LEFT JOIN track t on g.genre_id = t.genre_id
GROUP BY g.name