<template>
    <div class="py-5 px-5 bg-white">
        <div class="px-5">
            <div class="align-center">
                <h3 align-middle>Outbreak Progression</h3>
            </div>
            <div class="mx-5" align-middle>
                <div class="px-5 py-5">
                    <line-chart :data="progressionChartData(stateCumulativeData)" :points="false" width="800px" height="400px" class=""></line-chart>
                </div>
            </div>
            <div>
                <p>{{ currentState }} first reached 100 cases on {{ stateCumulativeData[0]['date_of_outbreak'] }}.</p>
            </div>
        </div>
    </div>
</template>

<script>
import {progressionChartData} from '~/mixins/helper.js'
export default {
    props: {
        currentState: {
            required: true
        },

        stateCumulativeData: {
            type: Array,
            required: true
        }
    },
    methods: {
        progressionChartData,
    }
}
</script>