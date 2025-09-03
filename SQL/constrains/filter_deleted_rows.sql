DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        SELECT table_name
        FROM information_schema.columns
        WHERE column_name = 'deleted_at' AND table_schema = 'public'
    LOOP
        EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY;', r.table_name);
        EXECUTE format(
            'CREATE POLICY active_only ON public.%I FOR SELECT USING (deleted_at IS NULL);',
            r.table_name
        );
    END LOOP;
END $$;
