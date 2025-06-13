CREATE OR REPLACE FUNCTION add_tracks_to_playlist(
    _playlist_id INTEGER,
    _playlist_tracks JSON
) RETURNS VOID AS $$
DECLARE
    track JSON;
    _track_id INTEGER;
BEGIN
    BEGIN
        FOR track IN SELECT * FROM json_array_elements(_playlist_tracks)
        LOOP
            _track_id := (track->>'track_id')::INTEGER;

            INSERT INTO playlist_track (playlist_id, track_id)
            VALUES (_playlist_id, _track_id);
        END LOOP;
    EXCEPTION WHEN OTHERS THEN
        RAISE EXCEPTION 'Error adding tracks to playlist: %', SQLERRM;
    END;
END;
$$ LANGUAGE plpgsql;
