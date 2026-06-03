import { createApp } from "vue";
import App from "./App.vue";
import Buefy from "buefy";
import "@fortawesome/fontawesome-free/css/solid.css";
import "@fortawesome/fontawesome-free/css/fontawesome.css";
import "buefy/dist/css/buefy.css";

createApp(App)
  .use(Buefy, {
    defaultIconPack: "fas",
  })
  .mount("#app");
