<template>
    <div class="px-5">
      <div class="mx-0 px-5">
        <b-card-group deck class="pt-5">
          <cumulative-cases-card :cumulativeCases="cumulativeCases"></cumulative-cases-card>
          <new-cases-chart-card :stateDailyData="nationalCumulative"></new-cases-chart-card>
          <cumulative-deaths-card :cumulativeDeaths="cumulativeDeaths"></cumulative-deaths-card>
        </b-card-group>
        <b-row class="py-4">
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
import {compareCases, numberWithCommas} from '~/mixins/helper.js'
import CumulativeCasesCard from '~/components/CumulativeCasesCard.vue'
import CumulativeDeathsCard from '~/components/CumulativeDeathsCard.vue'
import NewCasesChartCard from '~/components/NewCasesChartCard.vue'

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
    CumulativeCasesCard,
    CumulativeDeathsCard,
    NewCasesChartCard
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
  
  /* Method used by .sort() for sorting logic. Uses number of cases for sorting. */
  methods: {
    numberWithCommas,
  }
}
</script>