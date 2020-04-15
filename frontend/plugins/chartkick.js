import Vue from 'vue'
import Chartkick from 'vue-chartkick'
import Chart from 'chart.js'

Chartkick.configure({mapsApiKey: "AIzaSyBHf772lQ0UjEYK9QkjLevzWVXlBSedzvI"}) 

Vue.use(Chartkick.use(Chart))