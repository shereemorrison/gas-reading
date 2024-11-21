<script>
	import '../app.postcss';
	import { AppBar } from '@skeletonlabs/skeleton';

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

<slot />

<style>

.app-bar {
	display: flex;
	justify-content: center;  /* Center the logo horizontally */
	align-items: center;      /* Center the logo vertically */
	height: 50px;             /* Set the height of your app bar */
  }
  
  .logo {
	height: 50px; /* Adjust this size to match the height of your app bar */
  }
	nav a {
	margin-right: 20px;      /* Add spacing between the links */
	font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif; /* Change font */
	text-decoration: none;   /* Remove underline */
	color: inherit;          /* Inherit color from parent (adjust if needed) */
}

/* Remove margin from the last link */
nav a:last-child {
	margin-right: 0; }

</style>
