<template>
  <div>
    <div class="level">
      <div class="level-left">
        <b-button class="level-item" icon-left="upload" @click="confirmLoad">Load Configuration</b-button>
        <b-button class="level-item" icon-left="download" @click="confirmDeploy">Deploy Configuration</b-button>
      </div>
      <div class="level-right">
        <b-button class="level-item is-danger" icon-left="trash" @click="confirmDiscard"
          >Discard Configuration</b-button
        >
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <p class="title is-4">General</p>
        <b-field label="Application Logger Level">
          <b-select v-model="loggerLevel" placeholder="Select a level">
            <option v-for="option in LOGGER_LEVEL" :value="option" :key="option">
              {{ option }}
            </option>
          </b-select>
        </b-field>
      </div>
      <div class="column">
        <p class="title is-4">Smartmeters</p>
        <div class="block buttons">
          <b-button type="is-success" icon-left="plus" @click="addReader">Smartmeter</b-button>
        </div>
        <smart-meter
          v-for="(r, r_i) in readers"
          :key="r.id"
          :initConfig="r.config"
          @remove="removeReader(r_i)"
          @update="updateReader(r_i, $event)"
        />
      </div>
      <div class="column">
        <p class="title is-4">Data Sinks</p>
        <div class="block buttons">
          <b-button :disabled="loggerSink" type="is-success" icon-left="plus" @click="loggerSink = {}"
            >Logger Sink</b-button
          >
          <b-button :disabled="mqttSink" type="is-success" icon-left="plus" @click="mqttSink = {}">MQTT Sink</b-button>
        </div>
        <logger-sink
          v-if="loggerSink"
          :initConfig="loggerSink"
          @update="loggerSink = $event"
          @remove="loggerSink = null"
        />
        <mqtt-sink v-if="mqttSink" :initConfig="mqttSink" @update="mqttSink = $event" @remove="mqttSink = null" />
      </div>
    </div>
  </div>
</template>

<script>
import LoggerSink from "./LoggerSink.vue";
import MqttSink from "./MqttSink.vue";
import SmartMeter from "./SmartMeter.vue";
export default {
  components: { SmartMeter, LoggerSink, MqttSink },
  data() {
    return {
      loggerLevel: "WARNING",
      readers: [],
      loggerSink: null,
      mqttSink: null,
    };
  },
  created() {
    this.LOGGER_LEVEL = ["DEBUG", "INFO", "WARNING", "ERROR", "FATAL", "CRITICAL"];
  },
  methods: {
    addReader() {
      this.readers.push({
        id: this.getReaderId(),
        config: {},
      });
    },
    getReaderId() {
      if (this.readers.length == 0) {
        return 1;
      }
      return Math.max(...this.readers.map((r) => r.id)) + 1;
    },
    updateReader(index, newConfig) {
      this.readers[index].config = newConfig;
    },
    removeReader(index) {
      this.readers.splice(index, 1);
    },
    resetConfig() {
      this.loggerLevel = "WARNING";
      this.readers = [];
      this.loggerSink = null;
      this.mqttSink = null;
    },
    confirmDiscard() {
      this.$buefy.dialog.confirm({
        title: "Discard Configuration",
        message: "Do you want to reset the current configuration?",
        confirmText: "Reset",
        type: "is-danger",
        hasIcon: true,
        onConfirm: this.resetConfig,
      });
    },
    confirmLoad() {
      this.$buefy.dialog.confirm({
        title: "Load Configuration",
        message: "The current configuration will be overwritten.",
        confirmText: "Download",
        type: "is-danger",
        hasIcon: true,
        onConfirm: this.loadConfig,
      });
    },
    confirmDeploy() {
      this.$buefy.dialog.confirm({
        title: "Deploy Configuration",
        message: "Do you want to upload and deploy the configuration?",
        confirmText: "Upload",
        type: "is-danger",
        hasIcon: true,
        onConfirm: this.deployConfig,
      });
    },
  },
};
</script>

<style scoped></style>
