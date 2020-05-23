<template>
  <div v-enter-active>
    <b-navbar toggleable="lg" type="light" class="my-0 py-0 px-0">
      <b-navbar-brand class="mb-0 pb-4 pt-3" style="background-color: #532d8e;">
        <img src="https://floridapoly.edu/wp-content/themes/floridapolytechnic/images/logo.svg" width="250" height="40" alt="">
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse" class="mx-5"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto px-5">
          <b-nav-item href="#"><nuxt-link to="/">Home</nuxt-link></b-nav-item>
          <b-nav-item href="#"><nuxt-link to="/data">Data</nuxt-link></b-nav-item>
          <b-nav-item href="#"><nuxt-link to="/api">API</nuxt-link></b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    
    </b-navbar>
   
    <nuxt />
  </div>
</template>

<script>

</script>
<style>
html {
  font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}
</style>
