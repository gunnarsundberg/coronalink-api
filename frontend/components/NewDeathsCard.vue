<template>
    <b-card title="New Deaths" class="shadow" align="center">
        <b-card-text>
            <h1>{{ newDeaths }}</h1>
            <h3 class="text-danger" v-if="deathIncrease(newDeaths, initialDeaths) > 0 && isFinite(percentChange(initialDeaths, newDeaths))">+{{ percentChange(initialDeaths, newDeaths) }}%</h3>
            <h3 class="text-success" v-if="deathIncrease(newDeaths, initialDeaths) <= 0 && isFinite(percentChange(initialDeaths, newDeaths))">{{ percentChange(initialDeaths, newDeaths) }}%</h3>
        </b-card-text>
    </b-card>
</template>

<script>
import {deathIncrease, percentChange} from '~/mixins/helper.js'
export default {
    props: {
        newDeaths: {
            required: true
        },
        initialDeaths: {
            required: true
        }
    },
    methods: {
        deathIncrease,
        percentChange
    }
}
</script>