<script lang="ts">
	import '../app.postcss';
	import { AppBar } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';
	import supabaseClient from '$lib/supabase';
  
	let loggedIn = '';
	let cardNumbers: string[] = [];
  
	async function fetchAllCardNumbers() {
	  try {
		const { data, error } = await supabaseClient
		  .from('Members')
		  .select('cardnumber');
  
		if (error) {
		  console.error('Error fetching card numbers:', error);
		  return [];
		}
  
		if (data && data.length > 0) {
		  return data.map((row) => row.cardnumber); 
		} else {
		  return []; 
		}
	  } catch (err) {
		console.error('Error:', err);
		return []; 
	  }
	}
  
	async function checkLoginStatus(cardNumber: string) {
	  try {
		if (!cardNumber) {
		  console.log('No card number provided');
		  return false;
		}
  
		console.log('Checking login status for card:', cardNumber);
  
		const { data, error } = await supabaseClient
		  .from('Members') 
		  .select('logged_in') 
		  .eq('cardnumber', cardNumber); 
  
		if (error) {
		  console.error('Error fetching login status:', error);
		  return false;
		}
  
		console.log('Fetched data:', data);
  
		if (data && data.length > 0) {
		  return data[0]?.logged_in || false;
		} else {
		  console.log('No matching card number found in database');
		  return false;
		}
	  } catch (err) {
		console.error('Error:', err);
		return false;
	  }
	}
  
	onMount(async () => {
	  console.log('onMount triggered');
  
	  cardNumbers = await fetchAllCardNumbers();
  
	  if (cardNumbers.length > 0) {
		for (let cardNumber of cardNumbers) {
		  const status = await checkLoginStatus(cardNumber);
		  console.log(`Login status for ${cardNumber}:`, status);
		  if (status) {
			loggedIn = 'true'; 
			break;
		  }
		}
	  } else {
		console.log('No card numbers to check');
	  }
  
	  console.log('Logged in status:', loggedIn);
  
	  startLogoutTimer();
	});
  
	let timeoutId: NodeJS.Timeout;
  
	function startLogoutTimer() {

		timeoutId = setTimeout(async () => {
			
			for (let cardNumber of cardNumbers) {
			await supabaseClient
				.from("Members")
				.update({ logged_in: false })
				.eq("cardnumber", cardNumber);  
			
			console.log(`Logged out ${cardNumber} due to inactivity.`);
			}
			loggedIn = false; 
		}, 10000); // Timeout set to 15 minutes (900,000 milliseconds)
}
  
	function resetLogoutTimer() {
	  clearTimeout(timeoutId); 
	  startLogoutTimer(); 
	}
  
	async function scanCard(cardNumber: string) {
	  console.log("Card scanned:", cardNumber);
  
	  await supabaseClient
		.from('Members')
		.update({ logged_in: true })
		.eq('cardnumber', cardNumber); 
  
	  console.log(`Card ${cardNumber} scanned, logged in status updated.`);
	  loggedIn = 'true'; 
  
	  resetLogoutTimer();
	}
  
	onMount(() => {
	  supabaseClient
		.from('Members')
		.on('UPDATE', (payload) => {
		  // Only update the status if the card number matches the currently logged-in user
		  if (payload.new.cardnumber === cardNumbers[0]) {
			loggedIn = payload.new.logged_in ? 'true' : 'false';
			console.log(`Login status updated to: ${loggedIn}`);
		  }
		})
		.subscribe();
	});
  </script>
  
  <AppBar gridColumns="grid-cols-3" slotDefault="place-self-center" slotTrail="place-content-end">
	<svelte:fragment slot="lead"><img src="logo.png" alt="logo" class="logo"></svelte:fragment>
	
	<svelte:fragment slot="trail">
	  <nav>
		<a href="/">Home</a>
		<a href="/frequentlyaskedquestions">FAQ</a>
		<a href="/contactus">Contact Us</a>
	  </nav>
	</svelte:fragment>
  </AppBar>

  <header>
	{#if loggedIn === 'true'}
	  <p>Welcome back, Member!</p>
	  
	{:else}
	  <p>Please scan your card to log in.</p>
	  
	{/if}
  </header>
  
  <slot />
  
  <style>
	.logo {
	  height: 50px; 
	}
  
	nav a {
	  margin-right: 20px;    
	  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif; 
	  text-decoration: none;   
	  color: inherit;        
	}
  
	nav a:last-child {
	  margin-right: 0; 
	}
  </style>
  