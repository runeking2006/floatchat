SELECT * FROM public.argo_profiles

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'argo_profiles'