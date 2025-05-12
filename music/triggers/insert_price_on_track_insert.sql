CREATE OR REPLACE FUNCTION insert_price_on_track_insert()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO price (value, date, track_id)
  VALUES (NEW.unit_price, NOW(), NEW.track_id);

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_price_on_track_insert
AFTER INSERT ON track
FOR EACH ROW
EXECUTE FUNCTION insert_price_on_track_insert();
