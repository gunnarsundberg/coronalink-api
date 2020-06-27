<template>
    <div>
        <div>
            <div class="px-5 mx-0 py-5">
                <state-overview v-if="(dataLoaded(stateDailyData) && dataLoaded(stateCumulativeData))" :stateDailyData="stateDailyData" :stateCumulativeData="stateCumulativeData" :currentState="currentState"></state-overview>
            </div>
            <state-fast-facts v-if="dataLoaded(stateDemographics)" :currentState="currentState" :stateDemographics="stateDemographics"></state-fast-facts>
            <state-progression v-if="dataLoaded(stateDailyData)" :stateCumulativeData="stateCumulativeData" :stateDailyData="stateDailyData" :currentState="currentState" class="mx-0 bg-white"></state-progression>
        </div>
    </div>
</template>

<script>
import StateOverview from '~/components/StateOverview.vue'
import StateFastFacts from '~/components/StateFastFacts.vue'
import StateProgression from '~/components/StateProgression.vue'
import axios from 'axios'

export default {
    components: {
        StateOverview,
        StateFastFacts,
        StateProgression
    },

    props: {
        currentState: {
            required: true
        },
    },

    data() {
        return {
            stateDailyData: null,
            stateCumulativeData: null,
            stateDemographics: null,
        }
    },
  
    methods: {
        dataLoaded(data) {
            return (data != null)
        },

        /* Import outbreak data for a state (given in params). This is called each time a state is selected. */
        async updateStateData () {
            const stateDailyRequest = await axios.get('http://161.35.60.204/api/v1/outbreak/daily/states?state=' + this.currentState)
            const stateCumulativeRequest = await axios.get('http://161.35.60.204/api/v1/outbreak/cumulative/states?state=' + this.currentState)
            const stateDemographics = await axios.get('http://161.35.60.204/api/v1/demographics/states?state=' + this.currentState)
            
            this.stateDailyData = stateDailyRequest.data
            this.stateCumulativeData = stateCumulativeRequest.data
            this.stateDemographics = stateDemographics.data;
        },
    },
    
    created() {
        this.updateStateData()
    },

    watch: {
        currentState: function () {
            this.updateStateData()
        }
    },

}

</script>