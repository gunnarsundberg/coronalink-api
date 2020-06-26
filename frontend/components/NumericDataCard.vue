<template>
    <b-card :title="title" class="shadow" align="center" align-v="center">
        <b-card-text align-middle>
            <h1 class="py-5">{{ numericData }}</h1>
        </b-card-text>
        <template v-if="footerText" v-slot:footer>
            <small class="text-muted">{{ footerText }}</small>
        </template>
    </b-card>
</template>

<script>
export default {
    props: {
        numericData: {
            required: true
        },
        title: {
            required: true,
            type: String
        },
        footerText: {
            required: false,
        }
    }
}
</script>