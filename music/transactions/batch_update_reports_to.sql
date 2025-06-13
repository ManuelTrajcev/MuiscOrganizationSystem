CREATE OR REPLACE FUNCTION batch_update_reports_to(
    _updates JSON
) RETURNS VOID AS $$
DECLARE
    item JSON;
    _employee_id INTEGER;
    _reports_to_id INTEGER;
BEGIN
    BEGIN
        FOR item IN SELECT * FROM json_array_elements(_updates)
        LOOP
            _employee_id := (item->>'employee_id')::INTEGER;
            _reports_to_id := (item->>'reports_to_id')::INTEGER;

            UPDATE employee
            SET reports_to = _reports_to_id
            WHERE employee_id = _employee_id;

            IF NOT FOUND THEN
                RAISE EXCEPTION 'Employee with id % does not exist', _employee_id;
            END IF;
        END LOOP;
    EXCEPTION WHEN OTHERS THEN
        RAISE EXCEPTION 'Error updating reports_to: %', SQLERRM;
    END;
END;
$$ LANGUAGE plpgsql;
