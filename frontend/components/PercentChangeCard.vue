<template>
    <b-card :title="title" class="shadow" align="center">
        <b-card-text class="">
            <div class="py-4">
                <h1>{{ newData }}</h1>
                <h3 class="text-danger" v-if="displacement(newData, initialData) > 0 && isFinite(percentChange(initialData, newData))">+{{ percentChange(initialData, newData) }}%</h3>
                <h3 class="text-success" v-if="displacement(newData, initialData) <= 0 && isFinite(percentChange(initialData, newData))">{{ percentChange(initialData, newData) }}%</h3>
            </div>
        </b-card-text>
    </b-card>
</template>

<script>
import {displacement, percentChange} from '~/mixins/helper.js'
export default {
    props: {
        newData: {
            required: true,
        },

        initialData: {
            required: true,
        },

        title: {
            required: true,
            type: String
        }
    },
    methods: {
        displacement,
        percentChange
    }
}
</script>