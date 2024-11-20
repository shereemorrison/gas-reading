<script lang="ts">
    import supabaseClient from '$lib/supabase'
    
        let tableArr = [];
    
        async function getTemperature() {
            try {
                const { data, error } = await supabaseClient
                    .from('Temperature')
                    .select('reading, created_at');
    
                if (error) {
                    throw new Error(`Supabase error: ${error.message}`);
                }
    
                tableArr = data;
            } catch (err) {
                console.error("Error fetching temperature readings:", err.message);
            }
        }
    
        getTemperature();
    </script>
    
    <div class="container h-full mx-auto flex justify-center items-center">
        <div class="space-y-5">
            <h1 class="h1">Temperature Readings</h1>
        </div>
    </div>
    
    <div class="table-container">
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>Reading</th>
                    <th>Read At</th>
                </tr>
            </thead>
            <tbody>
                {#each tableArr as row}
                    <tr>
                        <td>{row.reading}</td>
                        <td>{row.created_at}</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
    
    <style>
        
        h1 {
            margin-top: 30px;
        }
    
      .table-container {
        display: flex;
        width: auto; 
        margin-top: 20px;
        align-items: center;
        margin-left: 37%;
        
      }
    
      table {
        width: auto; 
        table-layout: auto; 
        border-collapse: collapse; 
      }
    
    
    </style>
    