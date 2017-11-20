// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios';
import global_ from '@/commons/Global';
import VueHighlightJS from 'vue-highlight.js';
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(ElementUI);
Vue.use(VueHighlightJS);
Vue.config.productionTip = false;
Vue.prototype.$ELEMENT = { size: 'small' }
Vue.prototype.axios = axios;
Vue.prototype.GLOBAL = global_;

new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {App}
});
