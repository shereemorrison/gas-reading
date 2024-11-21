<h1>Frequently asked questions</h1>

<script>
    import { Accordion, AccordionItem } from "@skeletonlabs/skeleton";
</script>

<div class="accordion-container">
<Accordion class="accordion">
	<AccordionItem open>
		<svelte:fragment slot="summary">How did we get here?</svelte:fragment>
		<svelte:fragment slot="content">Was tasked with a simple project using micropython to read data from a gas reader (set up with ESP32), and a temperature reader (set up as a simulation on Wokwi), sending that data to Supabase, and then display it (using Svelte).  So, here we are! </svelte:fragment>
	</AccordionItem>
	<AccordionItem>
		<svelte:fragment slot="summary">Who are we?</svelte:fragment>
		<svelte:fragment slot="content">We are sensory overload </svelte:fragment>
	</AccordionItem>
    <AccordionItem>
		<svelte:fragment slot="summary">What else can I add?</svelte:fragment>
		<svelte:fragment slot="content">There's not much else to say, but I just really like this skeletonui accordion...</svelte:fragment>
	</AccordionItem>
	<!-- ... -->
</Accordion>
</div>

<style>
	h1 {
		text-align: center;
		margin-top: 50px;
	}
    .accordion-container {
        margin-top: 50px;
		margin-left: 100px;
		margin-right: 100px;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 8px;
		align-self: center;

    }

</style>