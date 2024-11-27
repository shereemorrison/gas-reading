import supabaseClient from '$lib/supabase';

let timeoutId: NodeJS.Timeout;
let cardNumbers: string[] = [];

export async function fetchAllCardNumbers() {
	try {
		const { data, error } = await supabaseClient.from('Members').select('cardnumber');
		if (error) {
			console.error('Error fetching card numbers:', error);
			return [];
		}
		return data?.map((row) => row.cardnumber) || [];
	} catch (err) {
		console.error('Error:', err);
		return [];
	}
}

export async function checkLoginStatus(cardNumber: string) {
	try {
		const { data, error } = await supabaseClient
			.from('Members')
			.select('logged_in')
			.eq('cardnumber', cardNumber);

		if (error) {
			console.error('Error fetching login status:', error);
			return false;
		}

		return data?.[0]?.logged_in || false;
	} catch (err) {
		console.error('Error:', err);
		return false;
	}
}

export function startLogoutTimer() {
	timeoutId = setTimeout(async () => {
		for (let cardNumber of cardNumbers) {
			await supabaseClient
				.from('Members')
				.update({ logged_in: false })
				.eq('cardnumber', cardNumber);

			console.log(`Logged out ${cardNumber} due to inactivity.`);
		}
	}, 900000); // 15 minutes (900,000 ms)
}

export function resetLogoutTimer() {
	clearTimeout(timeoutId);
	startLogoutTimer(); 
}

export async function scanCard(cardNumber: string) {
	console.log("Card scanned:", cardNumber);

	await supabaseClient
		.from('Members')
		.update({ logged_in: true })
		.eq('cardnumber', cardNumber);

	console.log(`Card ${cardNumber} scanned, logged in status updated.`);
	resetLogoutTimer(); 
}
