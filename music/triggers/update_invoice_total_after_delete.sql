CREATE OR REPLACE FUNCTION update_invoice_total_after_delete()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE invoice
    SET total = (
        SELECT COALESCE(SUM(unit_price * quantity), 0)
        FROM invoice_line
        WHERE invoice_id = OLD.invoice_id
    )
    WHERE invoice_id = OLD.invoice_id;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_invoice_total_after_delete
AFTER DELETE ON invoice_line
FOR EACH ROW
EXECUTE FUNCTION update_invoice_total_after_delete();
