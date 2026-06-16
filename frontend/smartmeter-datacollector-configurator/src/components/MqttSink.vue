<template>
  <div class="block box">
    <p class="level title is-5">
      <span class="level-left">MQTT Sink</span>
      <b-icon class="level-right" type="is-danger" icon="trash" @click.stop="$emit('remove')" />
    </p>
    <b-field label-position="inside" label="Host (IP/Hostname)">
      <b-input v-model="host" type="text" required placeholder="localhost" lazy></b-input>
    </b-field>
    <b-field label-position="inside" label="Port">
      <b-input v-model.number="port" required type="number" min="1" max="65535"></b-input>
    </b-field>
    <b-field>
      <b-checkbox v-model="tls">Use TLS protected connection</b-checkbox>
    </b-field>
    <b-field v-show="tls" label-position="inside" label="CA Certificate (optional)">
      <b-input
        custom-class="is-family-monospace has-background-white-ter is-size-7"
        v-model="caCert"
        type="textarea"
        placeholder="PEM formatted certificate"
        lazy></b-input>
    </b-field>
    <b-field v-show="caCert.trim()">
      <b-checkbox v-model="checkHostname">Check Hostname</b-checkbox>
    </b-field>
    <b-field>
      <b-checkbox v-model="authEnabled">Use Authentication</b-checkbox>
    </b-field>
    <b-field v-show="authEnabled" label-position="inside" label="MQTT Username">
      <b-input v-model="username" type="text" required lazy></b-input>
    </b-field>
    <b-field v-show="authEnabled" label-position="inside" label="MQTT Password">
      <b-input type="password" v-model="password" required lazy password-reveal></b-input>
    </b-field>
    <b-field>
      <b-checkbox v-model="rldspEnabled">
        Use standardized MQTT topic and payload (VSE RL-DSP CH 2024)
        <p v-show="rldspEnabled" class="is-size-7 has-text-info">
          Note: this format is incompatible with demo-application
        </p>
      </b-checkbox>
    </b-field>
    <b-field v-show="rldspEnabled" label-position="inside" label="Group in MQTT-topic (optional)">
      <b-input v-model="topicGroup" type="text" lazy></b-input>
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
      port: this.initConfig.port || 1883,
      tls: "tls" in this.initConfig ? this.initConfig.tls : false,
      caCert: this.initConfig.ca_cert || "",
      checkHostname: this.initConfig.check_hostname ? true : false,
      authEnabled: this.initConfig.username != null,
      username: this.initConfig.username || "",
      password: this.initConfig.password || "",
      topicGroup: this.initConfig.topic_group || "",
      rldspEnabled: this.initConfig.type === "mqttrldsp" ? true : false,
    };
  },
  computed: {
    config() {
      return {
        type: this.rldspEnabled ? "mqttrldsp" : "mqtt",
        host: this.host,
        port: this.port,
        tls: this.tls,
        ca_cert: this.caCert && this.tls ? this.caCert : null,
        check_hostname: this.checkHostname,
        username: this.authEnabled && this.username ? this.username : null,
        password: this.authEnabled && this.password ? this.password : null,
        topic_group: this.topicGroup,
      };
    },
  },
  watch: {
    config: {
      handler(value) {
        this.$emit("update", value);
      },
      immediate: true,
    },
  },
};
</script>

<style scoped></style>
