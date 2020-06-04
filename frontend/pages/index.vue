<template>
  <div class="mx-0 px-0 py-5">
    <div class="mb-5">
      <div class="pb-5">
          <h1 class="py-5 header" align="center">Poly COVID Tracking Project</h1>
          <div class="res-circle mb-5" align="center"></div>
      </div>
      <b-tabs align="center" class="pt-5">
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
      const {data} = await axios.get(process.env.API_HOST + process.env.PORT + '/api/v1/outbreak/cumulative/states')
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
/*
.res-circle {
  width: 20%;
  border-radius: 50%;
  background: #bcd6ff;
  position: absolute;
  margin: 60%;
  margin-top:-10%;
  z-index: 1;
}

.res-circle:after {
  content: "";
  display: block;
  padding-bottom: 100%;
  z-index: 1;
}
.header {
  z-index: 100 !important;
}
*/
</style>
