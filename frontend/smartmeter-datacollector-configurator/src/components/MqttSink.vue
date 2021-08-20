<template>
  <div class="block box">
    <p class="level title is-5">
      <span class="level-left">MQTT Sink</span>
      <b-icon class="level-right" type="is-danger" icon="trash" @click.native.stop="$emit('remove')" />
    </p>
    <b-field label-position="on-border" label="Host (IP/Hostname)">
      <b-input v-model="host" type="text" required placeholder="localhost" @input="update"></b-input>
    </b-field>
    <b-field label-position="on-border" label="Port">
      <b-input v-model.number="port" required type="number" min="1" max="65535" @input="update"></b-input>
    </b-field>
    <b-field>
      <b-checkbox v-model="tls" :value="false" @input="update">Use TLS protected connection</b-checkbox>
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
      host: this.initConfig.host || "",
      port: this.initConfig.port || "",
      tls: "tls" in this.initConfig ? this.initConfig.tls : false,
    };
  },
  created() {
    this.update();
  },
  methods: {
    update() {
      this.$emit("update", {
        type: "mqtt",
        host: this.host,
        port: this.port,
        tls: this.tls,
      });
    },
  },
};
</script>

<style scoped></style>
