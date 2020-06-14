<template>
  <div id="app">
    <Slide :closeOnNavigation="true" class="bg-dark">
      <a id="home">
        <span><nuxt-link to="/">Dashboard</nuxt-link></span>
      </a>
      <a id="">
        <span><nuxt-link to="/data">Data</nuxt-link></span>
      </a>
      <a id="">
        <span><nuxt-link to="/api">API</nuxt-link></span>
      </a>
    </Slide>
    <main id="page-wrap">
      <div class="px-5 py-5" style="background: #654ea3; background: -webkit-linear-gradient(to right, #654ea3, #eaafc8); background: linear-gradient(to right, #654ea3, #eaafc8);">
        <div class="my-0 py-5 px-5 text-white">
            <h1 class="pt-5 px-5 header">FLORIDA POLY</h1>
            <h1 class="pb-0 px-5 header">COVID PROJECT</h1>
            <p class=" px-5 pb-5">Data and insights related to the COVID-19 pandemic</p>
        </div>
      </div>
      <nuxt />
    </main>
  </div>
</template>

<style>
  .bm-burger-bars {
      background-color: white !important;
    }
  .line-style {
      position: absolute;
      height: 10% !important;
      left: 0;
      right: 0;
  }
  .bm-item-list > * > span {
      margin-left: 10px;
      font-weight: 700;
      color: white !important;
  }
  .bm-menu {
    background-color: #343a40 !important;
  } 
  .nuxt-link {
    color: white !important;
  }
  .header {
    font-family: 'Miriam Libre', sans-serif;
  }
  div {  
    font-family: 'Open Sans', sans-serif;
  }
</style>
