import Vue from 'vue'
import Chartkick from 'vue-chartkick'
import Chart from 'chart.js'

Chartkick.configure({mapsApiKey: "AIzaSyAVoZMoCXcDhEcm5YCY_G-yxVnq8ZyjWyY"})

Vue.use(Chartkick.use(Chart))