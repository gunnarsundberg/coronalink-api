<template>
    <b-card title="New Cases" class="shadow" align="center">
        <b-card-text class="">
            <div class="my-auto">
                <h1>{{ newCases }}</h1>
                <h3 class="text-danger" v-if="caseIncrease(newCases, initialCases) > 0 && isFinite(percentChange(initialCases, newCases))">+{{ percentChange(initialCases, newCases) }}%</h3>
                <h3 class="text-success" v-if="caseIncrease(newCases, initialCases) <= 0 && isFinite(percentChange(initialCases, newCases))">{{ percentChange(initialCases, newCases) }}%</h3>
            </div>
        </b-card-text>
    </b-card>
</template>

<script>
import {caseIncrease, percentChange} from '~/mixins/helper.js'
export default {
    props: {
        newCases: {
            required: true
        },
        initialCases: {
            required: true
        }
    },
    methods: {
        caseIncrease,
        percentChange
    }
}
</script>