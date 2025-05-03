CREATE OR REPLACE FUNCTION media_type_deletion()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.media_type_id = 1 THEN
        RAISE EXCEPTION 'Cannot delete default media type (MPEG audio file with id = 1).';
    END IF;

    UPDATE track
    SET media_type_id = 1
    WHERE media_type_id = OLD.media_type_id;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_media_type_deletion
BEFORE DELETE ON media_type
FOR EACH ROW
EXECUTE FUNCTION media_type_deletion();
