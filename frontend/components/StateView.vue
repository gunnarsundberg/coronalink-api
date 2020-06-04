<template>
    <div>
        <div class="d-flex justify-content-center pt-3" style="background: #f6f5f3;">
        </div>
        <div class="mx-0 bg-white">
            <div style="background: #f6f5f3;" class="px-5 mx-0">
                <div class="mx-0 px-5 mb-5">
                    <div class="row justify-content-between pb-0 mb-0">
                        <b-col>
                            <h3 v-if="dataLoaded(stateDailyData)">Overview</h3>
                            <h3 v-else>Select a State</h3>
                        </b-col>
                        <b-col class="float-right">
                            <b-form-select v-model="currentState" :options="states"  @change="updateStateData" class="w-50 mb-3 float-right"></b-form-select>
                        </b-col>
                    </div>
                    <p v-if="dataLoaded(stateDailyData)" class="text-muted pt-0">Data from {{ newestDate }}</p>
                </div>

                <state-dash-cards v-if="(dataLoaded(stateDailyData) && dataLoaded(stateCumulativeData))" :stateDailyData="stateDailyData" :stateCumulativeData="stateCumulativeData"></state-dash-cards>
               
            </div>

            <state-fast-facts v-if="dataLoaded(stateDailyData)" :currentState="currentState"></state-fast-facts>

            <state-progression v-if="dataLoaded(stateDailyData)" :stateCumulativeData="stateCumulativeData" :currentState="currentState"></state-progression>

        </div>
    </div>
</template>

<script>
import StateDashCards from '~/components/StateDashCards.vue'
import StateFastFacts from '~/components/StateFastFacts.vue'
import StateProgression from '~/components/StateProgression.vue'
import axios from 'axios'
import {progressionChartData} from '~/mixins/helper.js'

export default {
    components: {
        StateDashCards,
        StateFastFacts,
        StateProgression
    },

    props: {
        nationalOutbreak: {
            type: Array,
            required: true
        },
    },

    data() {
        return {
            states: [
                'AL', 
                'AK', 
                'AZ', 
                'AR', 
                'CA', 
                'CO', 
                'CT', 
                'DE', 
                'DC', 
                'FL', 
                'GA', 
                'HI', 
                'ID', 
                'IL', 
                'IN', 
                'IA', 
                'KS', 
                'KY', 
                'LA', 
                'ME', 
                'MD', 
                'MA', 
                'MI', 
                'MN', 
                'MS', 
                'MO', 
                'MT', 
                'NE', 
                'NV', 
                'NH', 
                'NJ', 
                'NM', 
                'NC', 
                'ND', 
                'OH', 
                'OK', 
                'OR', 
                'PA', 
                'RI', 
                'SC', 
                'SD', 
                'TN', 
                'TX', 
                'UT', 
                'VT', 
                'VA', 
                'WA', 
                'WV', 
                'WI', 
                'WY', 
                'NY',
        ],
            currentState: 'AL',
            stateDailyData: null,
            stateCumulativeData: null,
        }
    },

    computed: {
        newestDate: function () {
            return this.stateDailyData[0]['date']
        }

    },
  
  /* Method used by .sort() for sorting logic. Uses number of cases for sorting. */
    methods: {
        progressionChartData,

        dataLoaded(data) {
            return (data != null)
        },

        /* Import outbreak data for a state (given in params). This is called each time a state is selected. */
        async updateStateData (state) {
            const stateDailyRequest = await axios.get(process.env.API_HOST + process.env.PORT + '/api/v1/outbreak/daily/states?state=' + state)
            const stateCumulativeRequest = await axios.get(process.env.API_HOST + process.env.PORT + '/api/v1/outbreak/cumulative/historic/states?state=' + state)
            
            this.stateDailyData = stateDailyRequest.data
            this.stateCumulativeData = stateCumulativeRequest.data
        },
    }

}

</script>