CREATE OR REPLACE FUNCTION prevent_price_deletion()
RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'Deletion from price table is not allowed.';
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER trg_no_price_deletes
BEFORE DELETE ON price
FOR EACH ROW
EXECUTE FUNCTION prevent_price_deletion();
