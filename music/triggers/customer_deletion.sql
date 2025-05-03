CREATE OR REPLACE FUNCTION customer_deletion()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO deleted_customer_log (first_name, last_name, deleted_at)
    VALUES (OLD.first_name, OLD.last_name, NOW());
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_customer_deletion
AFTER DELETE ON customer
FOR EACH ROW
EXECUTE FUNCTION customer_deletion();