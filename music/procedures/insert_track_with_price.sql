CREATE OR REPLACE PROCEDURE insert_track_with_price(
    p_name VARCHAR,
    p_album_id INT,
    p_media_type_id INT,
    p_genre_id INT,
    p_composer VARCHAR,
    p_milliseconds INT,
    p_bytes INT,
    p_price NUMERIC(10,2)
)
LANGUAGE plpgsql
AS $$
DECLARE
    new_track_id INT;
BEGIN
    INSERT INTO track (
        name, album_id, media_type_id, genre_id, composer, milliseconds, bytes
    )
    VALUES (
        p_name, p_album_id, p_media_type_id, p_genre_id, p_composer, p_milliseconds, p_bytes
    )
    RETURNING track_id INTO new_track_id;

    INSERT INTO price (
        track_id, value, date
    )
    VALUES (
        new_track_id, p_price, NOW()
    );
END;
$$;

GRANT EXECUTE ON PROCEDURE insert_track_with_price(
    VARCHAR, INT, INT, INT, VARCHAR, INT, INT, NUMERIC
) TO PUBLIC;