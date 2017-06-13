import Vue from 'vue'
import Router from 'vue-router'
import Setting from '@/components/Setting'
import Detail from '@/components/Detail'
import LeakageData from '@/components/LeakageData'

Vue.use(Router);
const routes = [
  {path: '/', component: LeakageData},
  {path: '/view/tag/:tag', component: LeakageData},
  {path: '/view/leakage/:id', component: Detail},
  {path: '/setting', component: Setting},
];
export default new Router({
  routes
})
