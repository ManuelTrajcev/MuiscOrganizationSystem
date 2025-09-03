CREATE OR REPLACE FUNCTION merge_invoice_line()
RETURNS TRIGGER AS $$

BEGIN
    IF EXISTS (
        SELECT 1
        FROM invoice_line
        WHERE invoice_id = NEW.invoice_id
          AND track_id = NEW.track_id
    ) THEN
        UPDATE invoice_line
        SET quantity = quantity + NEW.quantity
        WHERE invoice_id = NEW.invoice_id
          AND track_id = NEW.track_id;

        RETURN NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_merge_invoice_line
BEFORE INSERT ON invoice_line
FOR EACH ROW
EXECUTE FUNCTION merge_invoice_line();
