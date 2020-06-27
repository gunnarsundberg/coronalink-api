<template>
    <div class="py-5 px-5 bg-white">
        <div class="px-5">
            <div class="align-center">
                <h3 align-middle>Outbreak Progression</h3>
            </div>
            <div class="mx-5">
                <div class="px-5 py-5" align="center">
                    <line-chart v-if="stateCumulativeHistoric" :data="caseChartData(stateCumulativeHistoric)" :points="false" width="800px" height="400px" class=""></line-chart>
                    <b-spinner v-else style="width: 3rem; height: 3rem;" label="Large Spinner"></b-spinner>
                </div>
            </div>
            <div>
                <p>{{ currentState }} first reached 100 cases on {{ stateCumulativeData[0]['date_of_outbreak'] }}.</p>
            </div>
        </div>
    </div>
</template>

<script>
import {caseChartData} from '~/mixins/helper.js'
import axios from 'axios'

export default {
    props: {
        currentState: {
            required: true
        },

        stateCumulativeData: {
            type: Array,
            required: true
        },

        stateDailyData: {
            type: Array,
            required: true
        }
    },

    data () {
        return {
            stateCumulativeHistoric: null,
            allStatesCumulativeHistoric: null
        }
    },

    methods: {
        caseChartData,

        async getCumulativeHistoricData() {
            const allStatesCumulativeRequest = await axios.get('http://161.35.60.204/api/v1/outbreak/cumulative/historic/states')
            const stateCumulativeHistoricRequest = await axios.get('http://161.35.60.204/api/v1/outbreak/cumulative/historic/states?state=' + this.currentState)
            this.allStatesCumulativeHistoric = allStatesCumulativeRequest.data
            this.stateCumulativeHistoric = stateCumulativeHistoricRequest.data
        }
    },

    created() {
        this.getCumulativeHistoricData()
    },
}
</script>