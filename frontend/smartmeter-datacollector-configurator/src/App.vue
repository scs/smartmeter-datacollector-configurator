<template>
  <div id="app" class="container is-fluid">
    <header class="level">
      <div class="level-left">
        <img class="image level-item is-128x128" alt="EKZ Logo" src="./assets/ekz_logo.png" />
      </div>
      <div class="level-right">
        <div class="level-item subtitle is-4">Smart Meter Data Collector Configurator</div>
      </div>
    </header>
    <configurator />
    <footer class="footer has-background-white">
      <p class="content has-text-centered">
        <a :href="grafanaUrl" target="_blank">Grafana Web</a> -
        <a href="https://github.com/scs/smartmeter-datacollector/wiki" target="_blank">Documentation</a> -
        <a href="https://github.com/scs/smartmeter-datacollector" target="_blank">Source Code</a>
      </p>
    </footer>
  </div>
</template>

<script>
import Configurator from "./components/Configurator.vue";
import { getGrafanaUrl } from "./utils";
export default {
  name: "App",
  components: {
    Configurator,
  },
  computed: {
    grafanaUrl: getGrafanaUrl,
  },
};
</script>

<style>
#app {
  font-family: Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  padding-top: 1rem;
}
</style>
