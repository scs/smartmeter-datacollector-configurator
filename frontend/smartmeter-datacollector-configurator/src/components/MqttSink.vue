<template>
  <div class="block box">
    <p class="level title is-5">
      <span class="level-left">MQTT Sink</span>
      <b-icon class="level-right" type="is-danger" icon="trash" @click.native.stop="$emit('remove')" />
    </p>
    <b-field label-position="on-border" label="Host (IP/Hostname)">
      <b-input v-model="host" type="text" required placeholder="localhost" lazy @input="update"></b-input>
    </b-field>
    <b-field label-position="on-border" label="Port">
      <b-input v-model.number="port" required type="number" min="1" max="65535" @input="update"></b-input>
    </b-field>
    <b-field>
      <b-checkbox v-model="tls" :value="false" @input="update">Use TLS protected connection</b-checkbox>
    </b-field>
    <b-field v-show="tls" label-position="on-border" label="CA Certificate (optional)">
      <b-input
        custom-class="is-family-monospace has-background-white-ter is-size-7"
        v-model="caCert"
        type="textarea"
        placeholder="PEM formatted certificate"
        lazy
        @input="update"
      ></b-input>
    </b-field>
    <b-field>
      <b-checkbox v-model="authEnabled" :value="false" @input="update">Use Authentication</b-checkbox>
    </b-field>
    <b-field v-show="authEnabled" label-position="on-border" label="Username">
      <b-input v-model="username" type="text" required lazy @input="update"></b-input>
    </b-field>
    <b-field v-show="authEnabled" label-position="on-border" label="Password (optional)">
      <b-input type="password" v-model="password" lazy password-reveal @input="update"></b-input>
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
      authEnabled: this.initConfig.username != null,
      username: this.initConfig.username || "",
      password: this.initConfig.password || "",
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
        ca_cert: this.caCert && this.tls ? this.caCert : null,
        username: this.authEnabled && this.username ? this.username : null,
        password: this.authEnabled && this.password ? this.password : null,
      });
    },
  },
};
</script>

<style scoped></style>
