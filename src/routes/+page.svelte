<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { fetchAllCardNumbers, checkLoginStatus } from '$lib/login';

	let isLoggedIn = false;

	onMount(async () => {
		const cardNumbers = await fetchAllCardNumbers();

		if (cardNumbers.length > 0) {
			for (let cardNumber of cardNumbers) {
				const status = await checkLoginStatus(cardNumber);
				if (status) {
					isLoggedIn = true;
					break;
				}
			}
		}

		if (isLoggedIn) {
			goto('/readings');
		}
	});
</script>

<p>Scan your card to login</p>
