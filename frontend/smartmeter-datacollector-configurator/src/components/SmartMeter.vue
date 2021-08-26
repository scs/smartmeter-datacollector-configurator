<template>
  <div class="block box">
    <p class="level title is-5">
      <span class="level-left">{{ TYPES[type] }}</span>
      <b-icon class="level-right" type="is-danger" icon="trash" @click.native.stop="$emit('remove')" />
    </p>
    <b-field label-position="on-border" label="Type">
      <b-select v-model="type" expanded placeholder="Select a smartmeter" @input="update">
        <option v-for="(name, typeKey) in TYPES" :value="typeKey" :key="typeKey">{{ name }}</option>
      </b-select>
    </b-field>
    <b-field v-show="customPort" label-position="on-border" label="Port/Device">
      <b-input v-model="port" type="text" required placeholder="/dev/ttyUSB0" lazy @input="update"></b-input>
    </b-field>
    <b-field v-show="!customPort" grouped label-position="on-border" label="TTY USB Devices">
      <b-select v-model="port" expanded @input="update">
        <option v-for="port in availablePorts" :value="port" :key="port">{{ port }}</option>
      </b-select>
      <b-button icon-right="sync-alt" @click="loadPorts" />
    </b-field>
    <b-field>
      <b-checkbox v-model="customPort" :value="false">Enter custom port</b-checkbox>
    </b-field>
    <b-field label-position="on-border" label="Decryption Key (optional)">
      <b-input v-model="key" type="text" lazy @input="update"></b-input>
    </b-field>
  </div>
</template>

<script>
import axios from "axios";
import { getBaseHostUrl } from "../utils";
export default {
  props: {
    initConfig: {
      type: Object,
      require: true,
    },
  },
  data() {
    return {
      id: this.initConfig.id,
      type: this.initConfig.type || "lge450",
      port: this.initConfig.port || "",
      key: this.initConfig.key || "",
      availablePorts: this.loadPorts(),
      customPort: false,
    };
  },
  created() {
    this.TYPES = {
      lge450: "L+G E450",
    };
    this.update();
  },
  methods: {
    update() {
      this.$emit("update", {
        type: this.type,
        port: this.port,
        key: this.key || null,
      });
    },
    loadPorts() {
      axios
        .get(`${getBaseHostUrl()}/ttydevices`, {
          timeout: 3000,
          responseType: "json",
        })
        .then((response) => {
          this.availablePorts = response.data;
        })
        .catch(() => {
          this.$buefy.toast.open({
            message: "Unable to retrieve available ports.",
            type: "is-danger",
            position: "is-top",
            duration: 4000,
          });
          this.availablePorts = [];
        });
    },
  },
};
</script>

<style scoped></style>
