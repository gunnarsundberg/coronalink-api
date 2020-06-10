<template>
  <div class="mx-0 px-0 py-5">
    <div class="mb-5">
      <div class="pb-5">
          <h1 class="py-5 header" align="center">Poly COVID Tracking Project</h1>
          <div class="res-circle mb-5" align="center"></div>
      </div>
      <b-tabs align="center" class="pt-5">
        <b-tab title="National View"><NationalView :nationalOutbreak="nationalOutbreak"></NationalView></b-tab>
        <b-tab title="State View"><StateView v-if="nationalOutbreak" :nationalOutbreak="nationalOutbreak"></StateView></b-tab>
      </b-tabs>
    </div>
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
      const {data} = await axios.get('http://161.35.60.204/api/v1/outbreak/cumulative/states')
      return {nationalOutbreak:data}
  },
}
</script>
<style>
</style>
