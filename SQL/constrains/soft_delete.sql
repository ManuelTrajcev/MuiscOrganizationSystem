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
    pk_col TEXT;
BEGIN
    FOR r IN (
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
    )
    LOOP
        SELECT kcu.column_name INTO pk_col
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON tc.constraint_name = kcu.constraint_name
         AND tc.table_name = kcu.table_name
        WHERE tc.constraint_type = 'PRIMARY KEY'
          AND tc.table_name = r.table_name
        LIMIT 1;

        IF pk_col IS NULL THEN
            RAISE NOTICE 'Table % has no primary key, skipping soft delete trigger', r.table_name;
            CONTINUE;
        END IF;

        EXECUTE format('ALTER TABLE public.%I ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;', r.table_name);

        EXECUTE format(
            'CREATE OR REPLACE FUNCTION soft_delete_%I()
             RETURNS TRIGGER AS $func$
             BEGIN
                 UPDATE %I SET deleted_at = NOW() WHERE %I = OLD.%I;
                 RETURN NULL;
             END;
             $func$ LANGUAGE plpgsql;',
            r.table_name, r.table_name, r.table_name, pk_col
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

