import Vue from 'vue'
import Router from 'vue-router'
// import Setting from '@/components/Setting'
// import Detail from '@/components/Detail'
// import LeakageData from '@/components/LeakageData'
const LeakageData = () => import('@/components/LeakageData');
const Detail = () => import('@/components/Detail');
const Setting = () => import('@/components/Setting');

Vue.use(Router);
const routes = [
  {path: '/', name: 'index', component: LeakageData},
  {path: '/view/tag/:tag', name: 'tag', component: LeakageData},
  {path: '/view/leakage/:id', component: Detail},
  {path: '/setting', name: 'setting', component: Setting},
];
export default new Router({
  routes
})
