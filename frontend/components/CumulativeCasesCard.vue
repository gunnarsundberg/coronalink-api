<template>
    <b-card title="Cumulative Cases" class="shadow" align="center" align-v="center">
        <b-card-text align-middle>
            <h1>{{ cumulativeCases }}</h1>
        </b-card-text>
    </b-card>
</template>

<script>
export default {
    props: {
        cumulativeCases: {
            required: true
        }
    }
}
</script>