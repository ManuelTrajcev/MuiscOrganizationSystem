CREATE OR REPLACE FUNCTION upsert_price()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Price p
        WHERE p.track_id = NEW.track_id
          AND p.date = NEW.date
    ) THEN
        UPDATE Price
        SET value = NEW.value
        WHERE track_id = NEW.track_id
          AND date = NEW.date;

        RETURN NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_upsert_price
BEFORE INSERT ON Price
FOR EACH ROW
EXECUTE FUNCTION upsert_price();
