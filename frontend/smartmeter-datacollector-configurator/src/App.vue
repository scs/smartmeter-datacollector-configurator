<template>
  <div id="app" class="container is-fluid">
    <header class="subtitle is-3">
      <div>Smart Meter Data Collector Configurator</div>
    </header>
    <configurator />
    <footer class="footer has-background-white">
      <p class="content has-text-centered">
        <a :href="grafanaUrl" target="_blank">Grafana Web</a> -
        <a href="https://github.com/scs/smartmeter-datacollector/wiki" target="_blank">Documentation</a> -
        <a href="https://github.com/scs/smartmeter-datacollector" target="_blank">Source Code</a>
      </p>
      <p class="content has-text-centered">
        Developed by
        <a href="https://www.scs.ch/" target="_blank">
          <img class="image is-32x32 is-inline mx-2" src="./assets/scs_logo.png" />
          Supercomputing Systems AG
        </a>
        on behalf of and funded by
        <a href="https://www.ekz.ch/" target="_blank">
          <img class="image is-32x32 is-inline mx-2" src="./assets/ekz_logo.png" />
          EKZ
        </a>
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
