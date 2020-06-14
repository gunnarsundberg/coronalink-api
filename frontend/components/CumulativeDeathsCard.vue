<template>
    <b-card title="Cumulative Deaths" class="shadow" align="center">
        <b-card-text>
            <h1>{{ cumulativeDeaths }}</h1>
        </b-card-text>
    </b-card>
</template>

<script>
export default {
    props: {
        cumulativeDeaths: {
            required: true
        }
    }
}
</script>