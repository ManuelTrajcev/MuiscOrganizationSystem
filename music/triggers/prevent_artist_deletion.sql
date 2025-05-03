CREATE OR REPLACE FUNCTION prevent_artist_deletion()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM album WHERE artist_id = OLD.artist_id
    ) THEN
        RAISE EXCEPTION 'Cannot delete artist with albums.';
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_artist_deletion
BEFORE DELETE ON artist
FOR EACH ROW
EXECUTE FUNCTION prevent_artist_deletion();
