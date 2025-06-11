--ADDING DELETED_AT COLUMN
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
    LOOP
        EXECUTE format('ALTER TABLE public.%I ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;', r.table_name);
    END LOOP;
END $$;

--SOFT DELETE TRIGGER
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
    )
    LOOP
        EXECUTE format(
            'CREATE OR REPLACE FUNCTION soft_delete_%I()
             RETURNS TRIGGER AS $func$
             BEGIN
                 UPDATE %I SET deleted_at = NOW() WHERE ctid = OLD.ctid;
                 RETURN NULL;
             END;
             $func$ LANGUAGE plpgsql;',
            r.table_name, r.table_name
        );

        EXECUTE format(
            'DROP TRIGGER IF EXISTS trg_soft_delete_%I ON %I;
             CREATE TRIGGER trg_soft_delete_%I
             BEFORE DELETE ON %I
             FOR EACH ROW
             EXECUTE FUNCTION soft_delete_%I();',
            r.table_name, r.table_name, r.table_name, r.table_name, r.table_name
        );
    END LOOP;
END $$;

