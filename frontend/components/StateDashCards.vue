<template>
    <div>
        <div>
            <b-card-group deck class="px-5">
                <new-cases-card :initialCases="initialCases" :newCases="newCases"></new-cases-card>
                <b-card title="New Cases This Week" class="shadow">
                    <div class="card-body">
                        <line-chart :data="weeklyChartData(stateDailyData)" height="150px"></line-chart>
                    </div>
                </b-card>
                <new-deaths-card :initialDeaths="initialDeaths" :newDeaths="newDeaths"></new-deaths-card>
            </b-card-group>

            <b-card-group deck class="pt-3 pb-5 px-5">
                <cumulative-cases-card :cumulativeCases="cumulativeCases"></cumulative-cases-card>
                <new-cases-chart-card :stateDailyData="stateDailyData"></new-cases-chart-card>
                <cumulative-deaths-card :cumulativeDeaths="cumulativeDeaths"></cumulative-deaths-card>
            </b-card-group>
        </div>
    </div>
</template>

<script>
import {numberWithCommas, progressionChartData} from '~/mixins/helper.js'
import NewCasesCard from '~/components/NewCasesCard.vue'
import NewDeathsCard from '~/components/NewDeathsCard.vue'
import CumulativeCasesCard from '~/components/CumulativeCasesCard.vue'
import CumulativeDeathsCard from '~/components/CumulativeDeathsCard.vue'
import NewCasesChartCard from '~/components/NewCasesChartCard.vue'

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

    components: {
        NewCasesCard,
        NewDeathsCard,
        CumulativeCasesCard,
        CumulativeDeathsCard,
        NewCasesChartCard
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

        weeklyChartData(stateDailyData) {
            var newWeeklyData = []
            for (var i=6; i >= 0; i--) {
                var newElement = [];
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