<template>
    <div>
      <div class="mx-0 px-0 my-5">
      <h3> Daily Overview</h3>
      <div class="row justify-content-between pb-4">
        <b-col class="col-4">
          <p class="text-muted">Data from 4/11/20</p>
        </b-col>
        <b-col class="col-4">
        </b-col>
      </div>

      <b-card-group deck v-if="dataLoaded(stateDailyData)">

        <b-card title="New Cases" class="shadow" align="center" align-v="center">
          <b-card-text align-middle>
            <h1>{{ newCases(stateDailyData) }}</h1>
            <h3 class="text-danger" v-if="caseIncrease(newCases(stateDailyData), initialCases(stateDailyData)) > 0">+{{ percentChange(initialCases(stateDailyData), newCases(stateDailyData)) }}%</h3>
            <h3 class="text-success" v-if="caseIncrease(newCases(stateDailyData), initialCases(stateDailyData)) <= 0">{{ percentChange(initialCases(stateDailyData), newCases(stateDailyData)) }}%</h3>
          </b-card-text>
        </b-card>

        <b-card title="Cases by Day" class="shadow">
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

      <b-card-group deck v-if="dataLoaded(stateDailyData)">

        <b-card title="New Cases" class="shadow" align="center" align-v="center">
          <b-card-text align-middle>
            <h1>{{ newCases(stateDailyData) }}</h1>
            <h3 class="text-danger" v-if="caseIncrease(newCases(stateDailyData), initialCases(stateDailyData)) > 0">+{{ percentChange(initialCases(stateDailyData), newCases(stateDailyData)) }}%</h3>
            <h3 class="text-success" v-if="caseIncrease(newCases(stateDailyData), initialCases(stateDailyData)) <= 0">{{ percentChange(initialCases(stateDailyData), newCases(stateDailyData)) }}%</h3>
          </b-card-text>
        </b-card>

        <b-card title="Cases by Day" class="shadow">
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

      <b-row class="py-3">
        
        <b-col class="col-lg-4 order-2-md">
          
            <b-card title="Top States by Cases" class="shadow mb-3">
              <div class="card-body">
                <ul class="list-group list-group-flush">
                  <li class="list-group-item">
                    <b-row class="">
                      <b-col class="">
                        <h5>State</h5>
                      </b-col>
                      <b-col class="float-right">
                        <h5 class="">Cases</h5>
                      </b-col>
                    </b-row>
                  </li>
                  <li v-for="state in nationalOutbreak.sort(compareCases).slice(0, 5)" :key="state['state']" class="list-group-item">
                    <b-row>
                      <b-col class="">
                        {{ state['state'] }}
                      </b-col>
                      <b-col class="float-right">
                        {{ numberWithCommas(state['cases']) }}
                      </b-col>
                    </b-row>
                  </li>
                </ul>
              </div>
            </b-card>

            
          
          
       
        </b-col>
        
        <b-col class="col-lg-8 order-1-md">
          <b-card title="Outbreak Map" class="shadow">
            <div class="card-body">
              <geo-chart :data="[['City', 'Cases'], ['US-FL', 70], ['US-NY', 90], ['US-CA', 42], ['US-OR', 51]]" :library="{region: 'US', resolution: 'provinces', sizeAxis: { minValue: 0, maxValue: 100 }, displayMode: 'markers'}"></geo-chart>
            </div>
          </b-card>
        </b-col>
      </b-row>
      <div class="py-5">
        <h3>Outbreak Progression</h3>
        <div>
          
          <ul>
            <li>State data</li>
            <p v-if="stateDailyData">{{ stateDailyData[0]['date'] }}</p>
            <li v-for="date in stateDailyData" class="item">
              State: {{ date['state'] }} Cases: {{ date['cases']}} Deaths: {{ date['deaths']}}
            </li>
          </ul> 
        </div>
      </div>
      </div>
    

  <script src="https://www.gstatic.com/charts/loader.js"></script>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: {
   nationalOutbreak: {
    type: Array,
    required: true
   }
  },

data() {
    return {
      states: [
        'AL', 
        'AK', 
        'AZ', 
        'AR', 
        'CA', 
        'CO', 
        'CT', 
        'DE', 
        'DC', 
        'FL', 
        'GA', 
        'HI', 
        'ID', 
        'IL', 
        'IN', 
        'IA', 
        'KS', 
        'KY', 
        'LA', 
        'ME', 
        'MD', 
        'MA', 
        'MI', 
        'MN', 
        'MS', 
        'MO', 
        'MT', 
        'NE', 
        'NV', 
        'NH', 
        'NJ', 
        'NM', 
        'NC', 
        'ND', 
        'OH', 
        'OK', 
        'OR', 
        'PA', 
        'RI', 
        'SC', 
        'SD', 
        'TN', 
        'TX', 
        'UT', 
        'VT', 
        'VA', 
        'WA', 
        'WV', 
        'WI', 
        'WY', 
        'NY',
        ],
      currentState: 'AL',
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
      const stateDailyRequest = await axios.get('http://161.35.60.204/api/v1/outbreak/daily/states?state=' + state)
      const stateCumulativeRequest = await axios.get('http://161.35.60.204/api/v1/outbreak/daily/states?state=' + state)
      this.stateDailyData = stateDailyRequest.data
      this.stateCumulativeData = stateCumulativeRequest.data
    },

    /* Live Data methods. These will be moved to a separate component in the future */
    percentChange(initialData, newData) {
        return ((newData - initialData)/initialData).toFixed(3) * 100
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
        for (var i=0; i < 7; i++) {
            var newElement = [];
            console.log(i)
            newElement[0] = stateDailyData[i]['date'] 
            newElement[1] = stateDailyData[i]['cases']
            newLiveChartData.push(newElement);
        }
        console.log(newLiveChartData)
        return newLiveChartData
    },

    
  }

}

</script>