CREATE OR REPLACE FUNCTION update_invoice_total_after_insert()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE invoice
    SET total = (
        SELECT COALESCE(SUM(il.quantity * lp.value), 0)
        FROM invoice_line il
        JOIN (
            SELECT DISTINCT ON (track_id)
                track_id, value
            FROM price
            ORDER BY track_id, date DESC
        ) lp ON il.track_id = lp.track_id
        WHERE il.invoice_id = NEW.invoice_id
    )
    WHERE invoice_id = NEW.invoice_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
