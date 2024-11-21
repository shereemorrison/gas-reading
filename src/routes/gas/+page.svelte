<script lang="ts">
    import { fetchReadings } from '$lib/fetchFunctions';

    let tableArr: any[] = [];
    let currentPage: number = 1;
    const resultsPerPage: number = 10;

    async function loadReadings(page: number) {
        const offset = (page - 1) * resultsPerPage;
        tableArr = await fetchReadings('Gas', resultsPerPage, offset);
    }

    function goToPage(page: number) {
        if (page < 1) return;
        currentPage = page;
        loadReadings(currentPage);
    }

    // Load the first page initially
    loadReadings(currentPage);

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

<div class="pagination">
    <button on:click={() => goToPage(currentPage - 1)} disabled={currentPage === 1}>
        Previous
    </button>
    <span>Page {currentPage}</span>
    <button on:click={() => goToPage(currentPage + 1)}>
        Next
    </button>
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

    .pagination {
        display: flex;
        justify-content: center;
        margin-top: 10px;
    }

    .pagination button {
        margin: 0 5px;
        padding: 5px 10px;
    }

    .pagination span {
        display: flex;
        align-items: center;
    }

    .pagination button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
</style>
