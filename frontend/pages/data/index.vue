<template>
  <div class="">
    <h1>Data</h1>
    <p>Overview and sources for our data</p>
    <div class="p-5 mx-lg-5">
        <div class="px-md-5 mx-md-5 px-sm-5">
            <h2>About</h2>
            <p>There are many sources of data on the Covid-19 outbreak. In our research team's attempts to get data to study the outbreak, we noticed that these datasets are fractured. In order to model the outbreak in terms of more than case and test numbers, researchers must aggregate data from many sources. We went through the pain of unifying these datasets so that you don't have to.
            Our goal in creating this open dataset is to remove one of the biggest barriers of scientific research while informing the public with easy visualizations and interpretations. This data was compiled by researchers at Florida Polytechnic University and is free to use for non-commercial purposes.</p>
            
            <h2>Overview</h2>
            <p>All of our outbreak, flight, and weather data available through the <a>API</a> is updated overnight (relative to EST). Because of timezone differences, updates will not be complete until 9AM the following day (possibly before). Although we provide some live data on the dashboard, the API data is NOT a live count. Records represent daily counts. Demographics and healthcare statistics will not be updated. For a complete list of available data, visit the <a>API Page</a></p>
            
            <h2>Covid-19 Outbreak Data</h2>
            <p>We currently have daily and cumulative outbreak data for all 50 states and the District of Columbia. We define an outbreak as 100 cases and have data beginning from the first day each state had 100 reported cases. We are working to provide county-level data in the near future.</p>
            <p>Source: <a href="https://covidtracking.com/" target="blank">The Covid Tracking Project</a></p>
            <p>See their website for any questions pertaining to data collection methods and terms of use.</p>
            
            <h2>Flight Data</h2>
            <p>Flight data is compiled by summing the number of inbound and outbound flights from all airports in each state with an IATA location identifier and timezone information available from OpenSky.</p>
            <p>Source: <a href="https://opensky-network.org/" target="blank">OpenSky Network</a></p>
            <p>See their website for any questions pertaining to data collection methods and terms of use.</p>
            
            <h2>Weather Data</h2>
            <p>State weather data is collected as an average of all weather data points from each county in the state. All data except for UV index is collected from Meteostat. UV index is collected from OpenWeatherMap.</p>
            <p>Source: <a href="https://meteostat.net/en" target="blank">Meteostat</a></p>
            <p>Source: <a href="https://openweathermap.org/" target="blank">OpenWeatherMap</a></p>
            <p>See their websites for any questions pertaining to data collection methods and terms of use.</p>

            <h2>Demographic Data</h2>
            <p>All state demographic data is compiled from the US Census Bureau's American Community Survey 5-Year, 2014-2018.</p>
            <p>Source: <a href="https://www.census.gov/data/developers/data-sets/acs-5year.html" target="blank">US Census Bureau</a></p>
            <p>See their website for any questions pertaining to data collection methods and terms of use.</p>

            <h2>Healthcare Data</h2>
            <p>This will be updated on completion of data collection.</p>
            <p>Source: <a href="" target="blank">TBD</a></p>
            <p>See their website for any questions pertaining to data collection methods and terms of use.</p>

            <h2>Our Team</h2>
            <p>Dr. Bayazit Karaman - Assistant Professor of Computer Science</p>
            <p>Gunnar Sundberg - Research Assistant</p>
            <p>Bryce Palmer - Research Assistant</p>
            <p>Dominic Nyfeler - Research Volunteer</p>

            <h2>Contact</h2>
            <p>If you encounter an issue with the application or would like to request a new feature, open a new issue on <a>the issues tab of our github page</a> and tag it as a bug, question, or enhancement, depending on which best suits your situation. If you would like to contact our team, reach out to <a href="mailto:bkaraman@floridapoly.edu">Dr. Bayazit Karaman</a> or <a href="mailto:gsundberg@floridapoly.edu">Gunnar Sundberg</a>.</p>
        </div>
    </div>
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