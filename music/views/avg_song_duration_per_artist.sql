CREATE VIEW  avg_track_duration_per_artist AS
SELECT ar.name as artist_name, concat(ceil(avg(milliseconds) / 1000), 's') as avg_track_duration_in_seconds
FROM artist ar
left join album al on ar.artist_id = al.album_id
left join track tr on al.album_id = tr.album_id
group by ar.name
order by ar.name