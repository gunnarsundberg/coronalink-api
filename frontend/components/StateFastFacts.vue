<template>
    <div class="bg-dark text-white px-5">
        <div class="px-5 py-5">
            <h3> {{ currentState }} Fast Facts</h3>

            <b-card-group deck class="px-5 py-5">

                <b-card class="shadow" bg-variant="dark" header="Population Density" text-variant="white">
                    <b-card-text align-middle>
                        
                    </b-card-text>
                </b-card>

                <b-card class="shadow" bg-variant="dark" header="Percent Over 60" text-variant="white">
                    <b-card-text>

                    </b-card-text>
                </b-card>

                <b-card class="shadow" bg-variant="dark" header="Hospital Beds" text-variant="white">
                    <b-card-text>
                        
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

    }
}
</script>