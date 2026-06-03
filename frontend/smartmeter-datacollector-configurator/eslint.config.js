import js from "@eslint/js";
import pluginVue from "eslint-plugin-vue";
import prettierConfig from "@vue/eslint-config-prettier";

export default [
  js.configs.recommended,
  ...pluginVue.configs["flat/essential"],
  prettierConfig,
  {
    rules: {
      "vue/multi-word-component-names": "off",
    },
  },
];
