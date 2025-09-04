CREATE VIEW most_listened_genre_per_customer AS
WITH genre_count AS
         (SELECT c.customer_id, c.first_name, c.last_name, g.name as genre, count(tr.track_id) as num_songs_per_genre
          FROM customer c
                   left join invoice i on c.customer_id = i.customer_id
                   left join invoice_line il on i.invoice_id = il.invoice_id
                   left join track tr on il.track_id = tr.track_id
                   left join genre g on tr.genre_id = g.genre_id
          where c.deleted_at is null
          group by c.customer_id, c.first_name, c.last_name, g.genre_id, g.name
          order by c.first_name, num_songs_per_genre desc),
     ranked_genres AS (SELECT *,
                              ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY num_songs_per_genre DESC) AS rn
                       FROM genre_count)
SELECT first_name, last_name, genre as most_listened_genre
FROM ranked_genres
WHERE rn = 1
ORDER BY first_name, last_name;