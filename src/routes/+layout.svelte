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
  
  .logo {
	height: 50px; 
  }
	nav a {
	margin-right: 20px;    
	font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif; 
	text-decoration: none;   
	color: inherit;        
}

nav a:last-child {
	margin-right: 0; }

</style>
