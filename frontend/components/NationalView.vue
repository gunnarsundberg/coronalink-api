<template>
    <div class="px-md-5">
      <div class="mx-0 px-5">
        <b-card-group deck class="pt-5">
          <numeric-data-card :numericData="cumulativeCases" title="Cumulative Cases"></numeric-data-card>
          <new-cases-chart-card :stateDailyData="nationalCumulative"></new-cases-chart-card>
          <numeric-data-card :numericData="cumulativeDeaths" title="Cumulative Deaths"></numeric-data-card>
        </b-card-group>
        <b-card-group deck class="pt-3">
            <b-card title="Top States by Cases" class="col-md-4 shadow">
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
          
            <b-card title="Outbreak Map" class="shadow col-md-8">
              <div class="card-body">
                <outbreak-map :stateCumulativeData="stateCumulative"></outbreak-map>
              </div>
            </b-card>
        </b-card-group>
        <div class="py-5">
        </div>
      </div>
  </div>
</template>

<script>
import {compareCases, numberWithCommas} from '~/mixins/helper.js'
import NumericDataCard from '~/components/NumericDataCard.vue'
import NewCasesChartCard from '~/components/NewCasesChartCard.vue'
import OutbreakMap from '~/components/OutbreakMap.vue'

export default {
  props: {
   nationalCumulative: {
    type: Array,
    required: true
   },
   stateCumulative: {
     type: Array,
     required: true
   }
  },

  components: {
    NumericDataCard,
    NewCasesChartCard,
    OutbreakMap
  },

  computed: {
    sortedNationalOutbreak: function () {
      return this.stateCumulative.sort(compareCases).slice(0, 5)
    },

    cumulativeCases: function() {
      return numberWithCommas(this.nationalCumulative[0]['positive'])
    },

    cumulativeDeaths: function() {
      return numberWithCommas(this.nationalCumulative[0]['death'])
    }
  },
  
  methods: {
    numberWithCommas,
  }
}
</script>