import Vue from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify'; // path to vuetify export
import { LMap, LTileLayer, LMarker, LTooltip, LPopup } from 'vue2-leaflet'
import 'leaflet/dist/leaflet.css'

Vue.config.productionTip = false;
Vue.component('l-map', LMap)
Vue.component('l-tile-layer', LTileLayer)
Vue.component('l-marker', LMarker)
Vue.component('l-tooltip', LTooltip)
Vue.component('l-popup', LPopup)

new Vue({
  vuetify,
  render: h => h(App),
}).$mount('#app');