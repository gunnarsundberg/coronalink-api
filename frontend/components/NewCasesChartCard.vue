<template>
    <b-card title="New Cases by Day" class="shadow">
        <div class="card-body">
            <column-chart :data="progressionChartData(stateDailyData)" min="0" :library="{scales: {xAxes: [{ticks: {display: false}}]}}" :label="false" height="150px"></column-chart>
        </div>
    </b-card>
</template>

<script>
import {progressionChartData} from '~/mixins/helper.js'
export default {
    props: {
        stateDailyData: {
            type: Array,
            required: true
        }
    },

    methods: {
        progressionChartData
    }
}
</script>