<template>
    <div>
        <div>
            <div class="px-5 mx-0 py-5">
                <state-dash-cards v-if="(dataLoaded(stateDailyData) && dataLoaded(stateCumulativeData))" :stateDailyData="stateDailyData" :stateCumulativeData="stateCumulativeData"></state-dash-cards>
            </div>
            <state-fast-facts v-if="dataLoaded(stateDemographics)" :currentState="currentState" :stateDemographics="stateDemographics"></state-fast-facts>
            <state-progression v-if="dataLoaded(stateDailyData)" :stateCumulativeData="stateCumulativeData" :currentState="currentState" class="mx-0 bg-white"></state-progression>
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
        currentState: {
            required: true
        }
    },

    data() {
        return {
            stateDailyData: null,
            stateCumulativeData: null,
            stateDemographics: null,
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
            const stateDailyRequest = await axios.get('http://161.35.60.204/api/v1/outbreak/daily/states?state=' + state)
            const stateCumulativeRequest = await axios.get('http://161.35.60.204/api/v1/outbreak/cumulative/historic/states?state=' + state)
            const stateDemographics = await axios.get('http://161.35.60.204/api/v1/demographics/states?state=' + state);
            
            this.stateDailyData = stateDailyRequest.data
            this.stateCumulativeData = stateCumulativeRequest.data
            this.stateDemographics = stateDemographics.data;
        },
    },
    mounted: function () {
        this.updateStateData(this.currentState)
    },
    updated: function () {
        this.updateStateData(this.currentState)
    }
}

</script>