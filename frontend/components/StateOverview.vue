<template>
    <div>
        <div>
            <b-card-group deck class="px-5">
                <numeric-data-card :numericData="cumulativeCases" title="Cumulative Cases"></numeric-data-card>
                <new-cases-chart-card :stateDailyData="stateDailyData"></new-cases-chart-card>
                <numeric-data-card :numericData="cumulativeDeaths" title="Cumulative Deaths"></numeric-data-card>
            </b-card-group>

            <b-card-group deck class="px-5 pt-3">
                <percent-change-card :initialData="initialCases" :newData="newCases" title="New Cases"></percent-change-card>
                <b-card title="New Cases This Week" class="shadow">
                    <div class="card-body">
                        <line-chart :data="weeklyChartData(stateDailyData)" height="150px"></line-chart>
                    </div>
                </b-card>
                <percent-change-card :initialData="initialDeaths" :newData="newDeaths" title="New Deaths"></percent-change-card>
            </b-card-group>

            <b-card-group deck class="px-5 pt-3">
                <b-card class="shadow" title="Cumulative Tests Performed">
                    <b-card-text align="center" class="py-5">
                        <h1>{{ cumulativeTotal }}</h1>
                    </b-card-text>
                    <b-link href="#" class="card-link" v-b-modal.testing-modal>Detailed Testing Information <b-icon-arrow-up-right-square></b-icon-arrow-up-right-square></b-link>
                    <b-modal id="testing-modal" size="xl" title="Testing">
                        <testing :stateDailyData="stateDailyData" :stateCumulativeData="stateCumulativeData" :currentState="currentState"></testing>
                        <template v-slot:modal-footer="{ ok }">
                            <b-button size="sm" variant="secondary" @click="ok()">
                                Close
                            </b-button>
                        </template>
                    </b-modal>
                </b-card>
                <b-card class="shadow" title="Tests Performed by Day">
                    <div class="card-body">
                        <column-chart :data="testingChartData(stateDailyData)" min="0" :library="{scales: {xAxes: [{ticks: {display: false}}]}}" :label="false" height="150px"></column-chart>
                    </div>
                </b-card>
                <numeric-data-card title="Cumulative Negative Tests" :numericData="cumulativeNegative"></numeric-data-card>
            </b-card-group>
        </div>
    </div>
</template>

<script>
import { numberWithCommas, testingChartData } from '~/mixins/helper.js'
import { BIconArrowUpRightSquare } from 'bootstrap-vue'
import PercentChangeCard from '~/components/PercentChangeCard.vue'
import NumericDataCard from '~/components/NumericDataCard.vue'
import NewCasesChartCard from '~/components/NewCasesChartCard.vue'
import Testing from '~/components/Testing.vue'

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

        currentState: {
            required: true
        }
    },

    components: {
        PercentChangeCard,
        NumericDataCard,
        NewCasesChartCard,
        Testing,
        BIconArrowUpRightSquare
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
        },

        cumulativeNegative: function () {
            return numberWithCommas(this.stateCumulativeData[0]['negative_tests'])
        },

        cumulativeTotal: function () {
            return numberWithCommas(this.stateCumulativeData[0]['total_tested'])
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

        testingChartData
    }
}
</script>