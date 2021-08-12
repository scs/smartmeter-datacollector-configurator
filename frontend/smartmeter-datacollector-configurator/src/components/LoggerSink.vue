<template>
  <div class="block box">
    <p class="level title is-5">
      <span class="level-left">Logger Sink</span>
      <b-icon class="level-right" type="is-danger" icon="trash" @click.native.stop="$emit('remove')" />
    </p>
    <p>Logs data to console.</p>
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
    this.config["name"] = this.initConfig.name || "DataLogger";
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
