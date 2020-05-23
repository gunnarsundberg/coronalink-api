<template>
    <div class="mx-0 px-0 my-5">
      <h3>Live</h3>
      <div class="row justify-content-between pb-4">
        <b-col class="col-4">
          <p class="text-muted">Data from 4/11/20</p>
        </b-col>
        <b-col class="col-4"></b-col>
      </div>

      <b-card-group deck v-if="dataLoaded(stateData)">

        <b-card title="New Cases" class="shadow" align="center" align-v="center">
          <b-card-text align-middle>
            <h1 v-if="newCases">{{ newCases }}</h1>
            <h3 class="text-danger" v-if="caseIncrease(newCases, initialCases(stateData)) > 0">+{{ percentChange(initialCases, newCases) }}%</h3>
            <h3 class="text-success" v-if="caseIncrease(newCases, initialCases(stateData)) <= 0">{{ percentChange(initialCases, newCases) }}%</h3>
          </b-card-text>
        </b-card>

        <b-card title="Cases by Day" class="shadow">
          <div class="card-body">
            <line-chart :data="{'2020-04-07': 130000, '2020-04-08': 135000, '2020-04-09': 160000, '2020-04-10': 190000, '2020-04-11': 191000, '2020-04-10': 190000}" height="150px" :min="100000"></line-chart>
          </div>
        </b-card>

        <b-card title="New Deaths" class="shadow" align="center">
          <b-card-text>
            <h1 v-if="newDeaths">{{ newDeaths }}</h1>
            <h3 class="text-danger" v-if="deathIncrease(newDeaths, initialDeaths(stateData)) > 0">+{{ percentChange(initialDeaths(stateData), newDeaths) }}%</h3>
            <h3 class="text-success" v-if="deathIncrease(newDeaths, initialDeaths(stateData)) <= 0">{{ percentChange(initialDeaths(stateData), newDeaths) }}%%</h3>
          </b-card-text>
        </b-card>

      </b-card-group>

    </div>
</template>

<script>
export default {
    mounted () {
        
    },

    props: {
        stateData: {
            type: Array,
            required: true
        },
        newCases: {
            default: 50,
            required: true
        },
        newDeaths: {
            default: 50,
            required: true
        }
    },

    data () {
        return {
            lastUpdated: null,
        }
    },

    methods: {
        percentChange(initialData, newData) {
            return ((newData - initialData)/initialData).toFixed(1)
        },

        deathIncrease(newDeaths, initialDeaths) {
            return newDeaths - initialDeaths
        },

        caseIncrease(newCases, initialCases) {
            return newCases - initialCases
        },

        initialCases(stateData) {
            return stateData[0]['cases']
        },
        initialDeaths(stateData) {
            stateData[0]['deaths']
        },

        dataLoaded(data) {
            console.log("Hello there")
            console.log(data)
            return (data != null)
        },
    },
}
</script>