<template>
    <div>
        <div class="d-flex justify-content-center pt-3" style="background: #f6f5f3;">
        </div>
        <div class="mx-0 bg-white">
            <div style="background: #f6f5f3;" class="px-5 mx-0">
                <div class="mx-0 px-0 mb-5">
                    <h3 v-if="dataLoaded(stateDailyData)"> Daily Overview</h3>
                    <h3 v-else>Select a State</h3>
                    <div class="row justify-content-between pb-4">
                        <b-col class="">
                            <p class="text-muted">Data from 4/11/20</p>
                        </b-col>
                        <b-col class="float-right">
                            <b-form-select v-model="currentState" :options="states"  @change="updateStateData" class="w-50 mb-3 float-right"></b-form-select>
                        </b-col>
                    </div>
                </div>
                <div v-if="dataLoaded(stateDailyData)">
                    <div>
                        <b-card-group deck class="px-5">

                            <b-card title="New Cases" class="shadow" align="center" align-v="center">
                                <b-card-text align-middle>
                                    <h1>{{ newCases(stateDailyData) }}</h1>
                                    <h3 class="text-danger" v-if="caseIncrease(newCases(stateDailyData), initialCases(stateDailyData)) > 0">+{{ percentChange(initialCases(stateDailyData), newCases(stateDailyData)) }}%</h3>
                                    <h3 class="text-success" v-if="caseIncrease(newCases(stateDailyData), initialCases(stateDailyData)) <= 0">{{ percentChange(initialCases(stateDailyData), newCases(stateDailyData)) }}%</h3>
                                </b-card-text>
                            </b-card>

                            <b-card title="New Cases This Week" class="shadow">
                                <div class="card-body">
                                    <line-chart :data="liveChartData(stateDailyData)" height="150px"></line-chart>
                                </div>
                            </b-card>

                            <b-card title="New Deaths" class="shadow" align="center">
                                <b-card-text>
                                    <h1>{{ newDeaths(stateDailyData) }}</h1>
                                    <h3 class="text-danger" v-if="deathIncrease(newDeaths(stateDailyData), initialDeaths(stateDailyData)) > 0">+{{ percentChange(initialDeaths(stateDailyData), newDeaths(stateDailyData)) }}%</h3>
                                    <h3 class="text-success" v-if="deathIncrease(newDeaths(stateDailyData), initialDeaths(stateDailyData)) <= 0">{{ percentChange(initialDeaths(stateDailyData), newDeaths(stateDailyData)) }}%</h3>
                                </b-card-text>
                            </b-card>

                        </b-card-group>

                        <b-card-group deck v-if="dataLoaded(stateDailyData)" class="pt-3 pb-5 px-5">

                            <b-card title="Cumulative Cases" class="shadow" align="center" align-v="center">
                                <b-card-text align-middle>
                                    <h1>{{ stateCumulativeData[0]['cases'] }}</h1>
                                </b-card-text>
                            </b-card>

                            <b-card title="New Cases by Day" class="shadow">
                                <div class="card-body">
                                    <column-chart :data="progressionChartData(stateDailyData)" min="0" :label="False" height="150px"></column-chart>
                                </div>
                            </b-card>

                            <b-card title="Cumulative Deaths" class="shadow" align="center">
                                <b-card-text>
                                    <h1>{{ stateCumulativeData[0]['deaths'] }}</h1>
                                </b-card-text>
                            </b-card>

                        </b-card-group>
                    </div>
                </div>
            </div>
                    <div v-if="dataLoaded(stateDailyData)" class="bg-dark text-white px-0">
                        <div class="px-5 py-5">
                            <h3> {{ currentState }} Fast Facts</h3>

                        </div>
                    </div>

                    <div v-if="dataLoaded(stateDailyData)" class="py-5 bg-white">
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
        <script src="https://www.gstatic.com/charts/loader.js"></script>
    </div>
</template>

<script>
import LiveData from '~/components/LiveData.vue'
import axios from 'axios'

export default {
  components: {
    LiveData
  },
  props: {
   nationalOutbreak: {
    type: Array,
    required: true
   }
  },

data() {
    return {
      states: [
        'Alabama', 
        'Alaska', 
        'Arizona', 
        'Arkansas', 
        'California', 
        'Colorado', 
        'Connecticut', 
        'Delaware', 
        'District of Columbia', 
        'Florida', 
        'Georgia', 
        'Hawaii', 
        'Idaho', 
        'Illinois', 
        'Indiana', 
        'Iowa', 
        'Kansas', 
        'Kentucky', 
        'Louisiana', 
        'Maine', 
        'Maryland', 
        'Massachusetts', 
        'Michigan', 
        'Minnesota', 
        'Mississippi', 
        'Missouri', 
        'Montana', 
        'Nebraska', 
        'Nevada', 
        'New Hampshire', 
        'New Jersey', 
        'New Mexico', 
        'North Carolina', 
        'North Dakota', 
        'Ohio', 
        'Oklahoma', 
        'Oregon', 
        'Pennsylvania', 
        'Rhode Island', 
        'South Carolina', 
        'South Dakota', 
        'Tennessee', 
        'Texas', 
        'Utah', 
        'Vermont', 
        'Virginia', 
        'Washington', 
        'West Virginia', 
        'Wisconsin', 
        'Wyoming', 
        'New York',
        ],
      currentState: 'Alabama',
      stateDailyData: null,
      stateCumulativeData: null,
    }
  },
  
  /* Method used by .sort() for sorting logic. Uses number of cases for sorting. */
  methods: {
    compareCases(a, b) {
      if (a['cases'] > b['cases']) return -1;
      if (b['cases'] > a['cases']) return 1;

      return 0;
    },
    
    /* Adds commas to make numbers pretty for displaying. */
    numberWithCommas(x) {
      return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },

    dataLoaded(data) {
        return (data != null)
    },

    /* Import outbreak data for a state (given in params). This is called each time a state is selected. */
    async updateStateData (state) {
      const stateDailyRequest = await axios.get('http://127.0.0.1:8000/api/v1/outbreak/daily/states?state=' + state)
      const stateCumulativeRequest = await axios.get('http://127.0.0.1:8000/api/v1/outbreak/cumulative/historic/states?state=' + state)
      this.stateDailyData = stateDailyRequest.data
      this.stateCumulativeData = stateCumulativeRequest.data
    },

    /* Live Data methods. These will be moved to a separate component in the future */
    percentChange(initialData, newData) {
        return ((((newData - initialData)/initialData) * 100).toFixed(1))
    },

    deathIncrease(newDeaths, initialDeaths) {
        return newDeaths - initialDeaths
    },

    caseIncrease(newCases, initialCases) {
        return newCases - initialCases
    },

    initialCases(stateDailyData) {
        return stateDailyData[1]['cases']
    },

    newCases(stateDailyData) {
        return stateDailyData[0]['cases']
    },

    initialDeaths(stateDailyData) {
        return stateDailyData[1]['deaths']
    },

    newDeaths(stateDailyData) {
        return stateDailyData[0]['deaths']
    },

    liveChartData(stateDailyData) {
        var newLiveChartData = []
        for (var i=6; i >= 0; i--) {
            var newElement = [];
            console.log(i)
            newElement[0] = stateDailyData[i]['date'] 
            newElement[1] = stateDailyData[i]['cases']
            newLiveChartData.push(newElement);
        }
        return newLiveChartData
    },

    progressionChartData(stateDailyData) {
        var newLiveChartData = []
        for (var i=0; i < stateDailyData.length; i++) {
            var newElement = [];
            console.log(i)
            newElement[0] = stateDailyData[i]['date'] 
            newElement[1] = stateDailyData[i]['cases']
            newLiveChartData.push(newElement);
        }
        return newLiveChartData
    },

    
  }

}

</script>