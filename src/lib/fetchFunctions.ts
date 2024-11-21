import supabaseClient from '$lib/supabase';

function formatTimestamp(timestamp: string): string {
    return new Date(timestamp).toLocaleString('en-GB', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
    });
}

export async function fetchReadings(tableName: string, limit: number, offset: number): Promise<any[]> {
    try {
        const { data, error } = await supabaseClient
            .from(tableName)
            .select('reading, created_at')
            .range(offset, offset + limit - 1); // Supabase uses 0-based indexing for range

        if (error) {
            throw new Error(`Supabase error: ${error.message}`);
        }

        // Format the timestamps in the fetched data
        return data?.map((row) => ({
            ...row,
            created_at: formatTimestamp(row.created_at),
        })) || [];
    } catch (err) {
        console.error(`Error fetching data from ${tableName}:`, err.message);
        return [];
    }
}
