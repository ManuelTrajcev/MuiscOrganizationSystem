CREATE OR REPLACE FUNCTION add_invoice_lines_to_existing_invoice(
    _invoice_id INTEGER,
    _invoice_lines JSON
) RETURNS VOID AS $$
DECLARE
    line JSON;
    _track_id INTEGER;
    _quantity INTEGER;
BEGIN
    BEGIN
        FOR line IN SELECT * FROM json_array_elements(_invoice_lines)
        LOOP
            _track_id := (line->>'track_id')::INTEGER;
            _quantity := (line->>'quantity')::INTEGER;

            INSERT INTO invoice_line (invoice_id, track_id, quantity)
            VALUES (_invoice_id, _track_id, _quantity);
        END LOOP;
    EXCEPTION WHEN OTHERS THEN
        RAISE EXCEPTION 'Error adding invoice lines: %', SQLERRM;
    END;
END;
$$ LANGUAGE plpgsql;