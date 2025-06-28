CREATE OR REPLACE FUNCTION prevent_genre_deletion()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM track WHERE genre_id = OLD.genre_id
    ) THEN
        RAISE EXCEPTION 'Cannot delete genre with a track of it.';
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_genre_deletion
BEFORE DELETE ON genre
FOR EACH ROW
EXECUTE FUNCTION prevent_genre_deletion();