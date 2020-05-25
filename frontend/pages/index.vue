<template>
  <div class="mx-0 px-0 py-5">
    <div class="mb-5">
      <h1 class="py-5" align="center">Poly COVID Tracking Project</h1>
      <b-tabs align="center">
        <b-tab title="National View"><NationalView v-if="nationalOutbreak" :nationalOutbreak="nationalOutbreak"></NationalView></b-tab>
        <b-tab title="State View"><StateView v-if="nationalOutbreak" :nationalOutbreak="nationalOutbreak"></StateView></b-tab>
      </b-tabs>
    </div>
    <script src="https://www.gstatic.com/charts/loader.js"></script>
  </div>
</template>

<script>
import StateView from '~/components/StateView.vue'
import NationalView from '~/components/NationalView.vue'
import axios from 'axios'

export default {
  components: {
    StateView,
    NationalView
  },
  data() {
    return {

    }
  },
  /* Initial import for national outbreak data. Called before initial page load. */
  async asyncData () {
      const {data} = await axios.get('http://127.0.0.1:8000/api/v1/outbreak/cumulative/states')
      return {nationalOutbreak:data}
  },
}
</script>
<style>
/*
.page-enter-active {
  -webkit-animation: color-change-2x 2s linear infinite alternate both;
	animation: color-change-2x 2s linear infinite alternate both;
}
@-webkit-keyframes color-change-2x {
  0% {
    background: #19dcea;
  }
  100% {
    background: #b22cff;
  }
}
@keyframes color-change-2x {
  0% {
    background: #19dcea;
  }
  100% {
    background: #b22cff;
  }
}
*/
</style>
