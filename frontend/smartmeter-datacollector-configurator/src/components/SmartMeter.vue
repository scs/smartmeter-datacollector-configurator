<template>
  <div class="block box">
    <p class="level title is-5">
      <span class="level-left">{{ TYPES[type] }}</span>
      <b-icon class="level-right" type="is-danger" icon="trash" @click.native.stop="$emit('remove')" />
    </p>
    <b-field label-position="on-border" label="Type">
      <b-select v-model="type" placeholder="Select a smartmeter" @input="update">
        <option v-for="(name, typeKey) in TYPES" :value="typeKey" :key="typeKey">{{ name }}</option>
      </b-select>
    </b-field>
    <b-field label-position="on-border" label="Port/Device">
      <b-input v-model="port" type="text" required placeholder="/dev/ttyUSB0" @input="update"></b-input>
    </b-field>
    <b-field label-position="on-border" label="Decryption Key (optional)">
      <b-input v-model="key" type="text" @input="update"></b-input>
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
      id: this.initConfig.id,
      type: this.initConfig.type || "lge450",
      port: this.initConfig.port || "",
      key: this.initConfig.key || "",
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
        key: this.key,
      });
    },
  },
};
</script>

<style scoped></style>
