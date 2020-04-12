import Vue from 'vue'
import Chartkick from 'vue-chartkick'
import Chart from 'chart.js'

Chartkick.configure({mapsApiKey: process.env.GOOGLE_MAPS_API_KEY})

Vue.use(Chartkick.use(Chart))