DROP TRIGGER IF EXISTS trg_customer_deletion ON customer;
DROP FUNCTION IF EXISTS customer_deletion();

CREATE OR REPLACE FUNCTION customer_deletion()
RETURNS TRIGGER AS $$
DECLARE
    total_spent NUMERIC(10, 2);
    invoice_count INTEGER;
BEGIN
    SELECT COALESCE(SUM(total), 0), COUNT(*)
    INTO total_spent, invoice_count
    FROM invoice
    WHERE customer_id = OLD.customer_id;

    INSERT INTO deleted_customer_log (
        first_name, last_name, deleted_at, total_spent, invoice_count
    )
    VALUES (
        OLD.first_name, OLD.last_name, NOW(), total_spent, invoice_count
    );

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_customer_deletion ON customer;

CREATE TRIGGER trg_customer_deletion
BEFORE DELETE ON customer
FOR EACH ROW
EXECUTE FUNCTION customer_deletion();
