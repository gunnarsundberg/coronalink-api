<template>
  <div class="mx-0 my-0 px-0" style="background: #f6f5f3;">
    <div class="px-4 pt-5">
      <div class="px-4">
        <h3 class="px-5">Overview</h3>
        <div class="row justify-content-between px-5">
          <p class="text-muted px-3">Data from {{ newestDate }}</p>
          <v-selectmenu :data="menu" :query="true" language="en" type="advanced" key-field="code" show-field="name" align="right" class="px-3" :title="title" v-model="currentRegion"></v-selectmenu>
        </div>
      </div>
    </div>
    <div>
      <NationalView v-if="currentRegion == 'US'" :nationalOutbreak="stateCumulative"></NationalView>
      <StateView v-if="isState(states,currentRegion)" :nationalOutbreak="stateCumulative" :currentState="currentRegion"></StateView>
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
      currentRegion: 'US',
      title: false,
      menu: [
        {
          title: 'National',
          list: [
            {code: 'US', name: 'United States'}
          ]
        },
        {
          title: 'State',
          list: []
        }
      ]
    }
  },
  /* Initial import for national outbreak data. Called before initial page load. */
  async asyncData () {
      const stateCumulative = await axios.get('http://161.35.60.204/api/v1/outbreak/cumulative/states')
      const states = await axios.get('http://161.35.60.204/api/v1/regions/states')
      return {stateCumulative: stateCumulative.data, states: states.data}
  },
  
  computed: {
    newestDate: function () {
      return this.stateCumulative[0]['date']
    }
  },

  methods: {
    getMenuStates: function (states) {
      var newStateMenu = []
      for (var i=0; i < states.length; i++) {
        var newStateInstance = {
          code: states[i]['code'],
          name: states[i]['name']
        }
        newStateMenu.push(newStateInstance)
      }
      return this.menu[1].list = newStateMenu
    },

    isState: function(states, regionCode) {
      let obj = states.find(o => o.code === regionCode);
      return obj != null
    }
  },

  mounted: function () {
    this.getMenuStates(this.states)
  }
}
</script>
<style>
  
</style>
