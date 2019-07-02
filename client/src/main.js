import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import "@/config/api";
import axios from "axios";
import VueHighlightJS from "vue-highlight.js";
import python from "highlight.js/lib/languages/python";
import Element from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import {b64Decode, timeAgo, toThousands, dateFormat} from "./utils";

Vue.use(VueHighlightJS, {
    languages: {
        python
    }
});
Vue.filter("b64Decode", b64Decode);
Vue.filter("timeAgo", timeAgo);
Vue.filter("dateFormat", dateFormat);
Vue.filter("toThousands", toThousands);
Vue.config.productionTip = false;
Vue.use(VueHighlightJS);
Vue.use(Element);
Vue.prototype.axios = axios;

new Vue({
    router,
    render: h => h(App)
}).$mount("#app");
