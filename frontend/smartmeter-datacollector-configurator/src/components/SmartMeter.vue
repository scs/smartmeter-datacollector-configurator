<template>
  <div class="block box">
    <p class="level title is-5">
      <span class="level-left">{{ TYPES[config.type] }}</span>
      <b-icon class="level-right" type="is-danger" icon="trash" @click.native.stop="$emit('remove')" />
    </p>
    <b-field label-position="on-border" label="Type">
      <b-select v-model="config.type" placeholder="Select a smartmeter">
        <option v-for="(name, type) in TYPES" :value="type" :key="type">{{ name }}</option>
      </b-select>
    </b-field>
    <b-field label-position="on-border" label="Port/Device">
      <b-input v-model="config.port" type="text" required placeholder="/dev/ttyUSB0"></b-input>
    </b-field>
    <b-field label-position="on-border" label="Decryption Key (optional)">
      <b-input v-model="config.key" type="text"></b-input>
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
    this.TYPES = {
      lge450: "L+G E450",
    };
    this.config["type"] = this.initConfig.type || "lge450";
    this.config["port"] = this.initConfig.port || "";
    this.config["key"] = this.initConfig.key || "";
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
