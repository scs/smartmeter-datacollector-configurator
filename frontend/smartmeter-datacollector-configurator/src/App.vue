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
  </div>
</template>

<script>
import Configurator from "./components/Configurator.vue";

export default {
  name: "App",
  components: {
    Configurator,
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
