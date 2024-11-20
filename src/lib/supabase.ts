import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://pywpljuuoecmoshimynl.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB5d3BsanV1b2VjbW9zaGlteW5sIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzE0NTI4NDAsImV4cCI6MjA0NzAyODg0MH0.kA_26qqxNGc4DUkeXALn2BnhCqcxbJbIyTAV_jvQzzU';

if (!SUPABASE_URL || !SUPABASE_KEY) {
    throw new Error('Supabase URL and key must be provided');
}

const supabaseClient = createClient(SUPABASE_URL, SUPABASE_KEY);

export default supabaseClient;


