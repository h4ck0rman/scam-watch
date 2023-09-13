<script>
  export let data;
  const { message } = data
  console.log(message)
  console.log('gotit')
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
<p>{message}</p>