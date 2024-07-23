<template>
  <v-app>
    <SurvivorManager />
  </v-app>
</template>

<script>
import SurvivorManager from './components/SurvivorManager.vue';

export default {
  name: 'App',
  components: {
    SurvivorManager
  }
};
</script>

<style>
@import '~vuetify/dist/vuetify.min.css';
@import "~leaflet/dist/leaflet.css";
</style>