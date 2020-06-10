<template>
    <div class="bg-dark text-white px-5">
        <div class="px-5 py-5">
            <h3> {{ currentState }} Fast Facts</h3>

            <b-card-group deck class="px-5 py-5" v-if="stateDemographics">

                <b-card class="shadow" bg-variant="dark" header="Population Density" text-variant="white">
                    <b-card-text align-middle>
                        <h1>{{ populationDensity }}</h1>
                        <p>persons per km<sup>2</sup></p>
                    </b-card-text>
                </b-card>

                <b-card class="shadow" bg-variant="dark" header="Percent Over 60" text-variant="white">
                    <b-card-text>
                        <h1>{{ percentOver60 }}</h1>
                    </b-card-text>
                </b-card>

                <b-card class="shadow" bg-variant="dark" header="Median Age" text-variant="white">
                    <b-card-text>
                        <h1>{{ medianAge }}</h1>
                    </b-card-text>
                </b-card>

            </b-card-group>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        currentState: {
            required: true
        },
        stateDemographics: {
            required: true
        }
    },
    
    computed: {
        percentOver60: function () {
            return this.stateDemographics[0]['percent_60s'] + this.stateDemographics[0]['percent_70s'] + this.stateDemographics[0]['percent_80_plus']
        },
        populationDensity: function () {
            return this.stateDemographics[0]['population_density']
        },
        medianAge: function () {
            return this.stateDemographics[0]['median_age']
        }
    },
    methods: {
        
    }
}
</script>