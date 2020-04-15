<template>
  <div class="mx-0 px-5 py-5" style="background: #f6f5f3;">
    <div class="mx-0 px-0">
      <div class="row justify-content-between pb-4">
        <b-col class="col-4">
          <p class="text-muted">Data from 4/11/20</p>
        </b-col>
        <b-col class="col-4">
          <b-dropdown id="dropdown-1" text="View" class="m-md-2 float-right">
            <b-dropdown-item>National View</b-dropdown-item>
            <b-dropdown-item>State View</b-dropdown-item>
          </b-dropdown>
        </b-col>
      </div>
      <b-card-group deck>
        <b-card title="New Cases" class="shadow" align="center" align-v="center">
          <b-card-text>
            <h1>34,458</h1>
            <h3 class="text-danger">+9.7%</h3>
          </b-card-text>
        </b-card>

        <b-card title="Cases by Day" class="shadow">
          <div class="card-body">
            <line-chart :data="{'2020-04-07': 130000, '2020-04-08': 135000, '2020-04-09': 160000, '2020-04-10': 190000, '2020-04-11': 191000, '2020-04-10': 190000}" height="150px" :min="100000"></line-chart>
          </div>
        </b-card>

        <b-card title="New Deaths" class="shadow" align="center">
          <b-card-text>
            <h1>1,458</h1>
            <h3 class="text-danger">+6.3%</h3>
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
                      <b-col class="">
                        <h5 class="mr-0 ml-5">Cases</h5>
                      </b-col>
                    </b-row>
                  </li>
                  <li class="list-group-item">
                    <b-row>
                      <b-col class="col-8">
                        New York
                      </b-col>
                      <b-col class="col-4">
                        72,124
                      </b-col>
                    </b-row>
                  </li>
                  <li class="list-group-item">
                    <b-row>
                      <b-col class="col-8">
                        New Jersey
                      </b-col>
                      <b-col class="col-4">
                        29,444
                      </b-col>
                    </b-row>
                  </li>
                  <li class="list-group-item">
                    <b-row>
                      <b-col class="col-8">
                        Pennsylvania
                      </b-col>
                      <b-col class="col-4">
                        18,492
                      </b-col>
                    </b-row>
                  </li>
                  <li class="list-group-item">
                    <b-row>
                      <b-col class="col-8">
                        Massachussetts
                      </b-col>
                      <b-col class="col-4">
                        16,577
                      </b-col>
                    </b-row>
                  </li>
                  <li class="list-group-item">
                    <b-row>
                      <b-col class="col-8">
                        California
                      </b-col>
                      <b-col class="col-4">
                        15,788
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
    </div>

  <script src="https://www.gstatic.com/charts/loader.js"></script>

  </div>
</template>

<script>
import Logo from '~/components/Logo.vue'

export default {
  components: {
    Logo
  }
}

</script>

<style>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>
