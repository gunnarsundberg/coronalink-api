<template>
    <div>
        <div>
            <b-card-group deck class="px-5">

                <b-card title="New Cases" class="shadow" align="center">
                    <b-card-text class="">
                        <div class="my-auto">
                        <h1>{{ newCases }}</h1>
                        <h3 class="text-danger" v-if="caseIncrease(newCases, initialCases) > 0">+{{ percentChange(initialCases, newCases) }}%</h3>
                        <h3 class="text-success" v-if="caseIncrease(newCases, initialCases) <= 0">{{ percentChange(initialCases, newCases) }}%</h3>
                        </div>
                    </b-card-text>
                </b-card>

                <b-card title="New Cases This Week" class="shadow">
                    <div class="card-body">
                        <line-chart :data="weeklyChartData(stateDailyData)" height="150px"></line-chart>
                    </div>
                </b-card>

                <b-card title="New Deaths" class="shadow" align="center">
                    <b-card-text>
                        <h1>{{ newDeaths }}</h1>
                        <h3 class="text-danger" v-if="deathIncrease(newDeaths, initialDeaths) > 0">+{{ percentChange(initialDeaths, newDeaths) }}%</h3>
                        <h3 class="text-success" v-if="deathIncrease(newDeaths, initialDeaths) <= 0">{{ percentChange(initialDeaths, newDeaths) }}%</h3>
                    </b-card-text>
                </b-card>

            </b-card-group>

            <b-card-group deck class="pt-3 pb-5 px-5">

                <b-card title="Cumulative Cases" class="shadow" align="center" align-v="center">
                    <b-card-text align-middle>
                        <h1>{{ cumulativeCases }}</h1>
                    </b-card-text>
                </b-card>

                <b-card title="New Cases by Day" class="shadow">
                    <div class="card-body">
                        <column-chart :data="progressionChartData(stateDailyData)" min="0" :library="{scales: {xAxes: [{ticks: {display: false}}]}}" :label="False" height="150px"></column-chart>
                    </div>
                </b-card>

                <b-card title="Cumulative Deaths" class="shadow" align="center">
                    <b-card-text>
                        <h1>{{ cumulativeDeaths }}</h1>
                    </b-card-text>
                </b-card>

            </b-card-group>
        </div>
    </div>
</template>

<script>
import {numberWithCommas, progressionChartData} from '~/mixins/helper.js'

export default {
    props: {
        stateDailyData: {
            type: Array,
            required: true
        },

        stateCumulativeData: {
            type: Array,
            required: true
        },

    },

    data () {
        return {

        }
    },

    computed: {
        /* Section: Day-over-day values */
        initialCases: function() {
            return numberWithCommas(this.stateDailyData[1]['cases'])
        },

        newCases: function() {
            return numberWithCommas(this.stateDailyData[0]['cases'])
        },

        initialDeaths: function() {
            return numberWithCommas(this.stateDailyData[1]['deaths'])
        },

        newDeaths: function() {
            return numberWithCommas(this.stateDailyData[0]['deaths'])
        },

        /* Section: Cumulative values */
        cumulativeCases: function() {
            return numberWithCommas(this.stateCumulativeData[0]['cases'])
        },

        cumulativeDeaths: function() {
            return numberWithCommas(this.stateCumulativeData[0]['deaths'])
        }

    },
    
    methods: {
        /* Live Data methods. These will be moved to a separate component in the future */
        percentChange(initialData, newData) {
            return ((((newData - initialData)/initialData) * 100).toFixed(1))
        },

        deathIncrease(newDeaths, initialDeaths) {
            return newDeaths - initialDeaths
        },

        caseIncrease(newCases, initialCases) {
            return newCases - initialCases
        },

        weeklyChartData(stateDailyData) {
            var newWeeklyData = []
            for (var i=6; i >= 0; i--) {
                var newElement = [];
                console.log(i)
                newElement[0] = stateDailyData[i]['date'] 
                newElement[1] = stateDailyData[i]['cases']
                newWeeklyData.push(newElement);
            }
            return newWeeklyData
        },

        progressionChartData
    }
}
</script>