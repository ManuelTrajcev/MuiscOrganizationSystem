CREATE OR REPLACE FUNCTION prevent_deletion_of_default_media_type()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.media_type_id = 1 THEN
        RAISE EXCEPTION 'Cannot delete default media type (id = 1)';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_deletion_of_default_media_type
BEFORE DELETE ON media_type
FOR EACH ROW
EXECUTE FUNCTION prevent_deletion_of_default_media_type();
