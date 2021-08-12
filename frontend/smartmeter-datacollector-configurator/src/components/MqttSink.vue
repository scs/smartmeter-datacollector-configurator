<template>
  <div class="block box">
    <p class="level title is-5">
      <span class="level-left">MQTT Sink</span>
      <b-icon class="level-right" type="is-danger" icon="trash" @click.native.stop="$emit('remove')" />
    </p>
    <b-field label-position="on-border" label="Host (IP/Hostname)">
      <b-input v-model="config.host" type="text" required placeholder="localhost"></b-input>
    </b-field>
    <b-field label-position="on-border" label="Port">
      <b-input v-model.number="config.port" required type="number" min="1" max="65535"></b-input>
    </b-field>
    <b-field>
      <b-checkbox v-model="config.tls" :value="false">Use TLS protected connection</b-checkbox>
    </b-field>
  </div>
</template>

<script>
export default {
  props: {
    initConfig: {
      type: Object,
      require: true,
    },
  },
  data() {
    return {
      config: {},
    };
  },
  created() {
    this.config["host"] = this.initConfig.type || "";
    this.config["port"] = this.initConfig.port || "";
    if ("tls" in this.initConfig) {
      this.config["tls"] = this.initConfig["tls"];
    } else {
      this.config["tls"] = false;
    }
  },
  watch: {
    config: {
      handler: function () {
        this.$emit("update", this.config);
      },
      deep: true,
    },
  },
};
</script>

<style scoped></style>
