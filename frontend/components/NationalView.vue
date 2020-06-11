<template>
    <div class="px-5">
      <div class="mx-0 px-4 my-5">
      <h3>Overview</h3>
      <div class="row justify-content-between pb-4">
        <b-col class="col-4">
          <p class="text-muted">Data from {{ newestDate }}</p>
        </b-col>
        <b-col class="col-4">
        </b-col>
      </div>

      <b-row class="py-3">
        
        <b-col class="col-lg-4 order-2-md">
          
          <b-card title="Top States by Cases" class="shadow mb-3">
            <div class="card-body">
              <ul class="list-group list-group-flush">
                <li class="list-group-item">
                  <b-row class="">
                    <b-col class="">
                      <h5>State</h5>
                    </b-col>
                    <b-col class="float-right">
                      <h5 class="">Cases</h5>
                    </b-col>
                  </b-row>
                </li>
                <li v-for="state in sortedNationalOutbreak" :key="state['state']" class="list-group-item">
                  <b-row>
                    <b-col class="">
                      {{ state['state'] }}
                    </b-col>
                    <b-col class="float-right">
                      {{ numberWithCommas(state['cases']) }}
                    </b-col>
                  </b-row>
                </li>
              </ul>
            </div>
          </b-card>

        </b-col>
        
        <b-col class="col-lg-8 order-1-md">
          <b-card title="Outbreak Map" class="shadow">
            <div class="card-body">
              <geo-chart :data="[['City', 'Cases'], ['US-FL', 70], ['US-NY', 90], ['US-CA', 42], ['US-OR', 51]]" :library="{region: 'US', resolution: 'provinces', sizeAxis: { minValue: 0, maxValue: 100 }, displayMode: 'markers'}"></geo-chart>
            </div>
          </b-card>
        </b-col>
      </b-row>
      <div class="py-5">
      </div>
      </div>
  </div>
</template>

<script>
import {compareCases} from '~/mixins/helper.js'

export default {
  props: {
   nationalOutbreak: {
    type: Array,
    required: true
   }
  },

  data() {
      return {
      }
  },

  computed: {
    sortedNationalOutbreak: function () {
      return this.nationalOutbreak.sort(compareCases).slice(0, 5)
    },
    
    newestDate: function () {
      return this.nationalOutbreak[0]['date']
    }
  },
  
  /* Method used by .sort() for sorting logic. Uses number of cases for sorting. */
  methods: {
    /* Adds commas to make numbers pretty for displaying. */
    numberWithCommas(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    
  }

}

</script>