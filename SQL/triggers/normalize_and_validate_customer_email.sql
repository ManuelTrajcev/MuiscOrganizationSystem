CREATE OR REPLACE FUNCTION normalize_and_validate_customer_email()
RETURNS TRIGGER AS $$
BEGIN
    NEW.email := LOWER(NEW.email);

    IF NEW.email !~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Invalid email format: %', NEW.email;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_normalize_validate_email
BEFORE INSERT ON customer
FOR EACH ROW
EXECUTE FUNCTION normalize_and_validate_customer_email();