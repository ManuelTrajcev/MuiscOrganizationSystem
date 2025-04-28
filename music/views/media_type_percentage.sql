CREATE VIEW media_type_percentage AS
with cte as (SELECT count(track_id) as total
             FROM media_type mt
                      left join track tr on mt.media_type_id = tr.media_type_id)
SELECT mt.name                                          as media_type,
       count(tr.track_id)                               as num_of_tracks,
       round(count(tr.track_id) * 100.0 / cte.total, 2) as percentage
FROM media_type mt
         left join track tr on mt.media_type_id = tr.media_type_id
         cross join cte
group by mt.media_type_id, mt.name, cte.total
order by percentage desc
