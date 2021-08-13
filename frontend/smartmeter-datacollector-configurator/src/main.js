import Vue from "vue";
import App from "./App.vue";
import Buefy from "buefy";
import "@fortawesome/fontawesome-free/css/solid.css";
import "@fortawesome/fontawesome-free/css/fontawesome.css";
import "buefy/dist/buefy.min.css";

Vue.config.productionTip = false;
Vue.use(Buefy, {
  defaultIconPack: "fas",
});

new Vue({
  render: (h) => h(App),
}).$mount("#app");
