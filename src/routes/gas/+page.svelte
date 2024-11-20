<script lang="ts">
import supabaseClient from '$lib/supabase'

        let tableArr = [];
    
        async function getReadings() {
            try {
                const { data, error } = await supabaseClient
                    .from('Gas')
                    .select('reading, created_at');
    
                if (error) {
                    throw new Error(`Supabase error: ${error.message}`);
                }
    
                tableArr = data;
            } catch (err) {
                console.error("Error fetching gas readings:", err.message);
            }
        }
    
        getReadings();
    </script>
    
    <div class="container h-full mx-auto flex justify-center items-center">
        <div class="space-y-5">
            <h1 class="h1">Gas Readings</h1>
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
    