import Vue from "vue";
import Router from "vue-router";

const LeakageData = () => import("@/views/result/Index");
const Detail = () => import("@/views/result/Detail");
const Setting = () => import("@/views/setting/Setting");

Vue.use(Router);
const routes = [
    {
        path: "/", name: "index", meta: {name: '首页'}, component: LeakageData
    },
    {path: "/view/leakage/:id", name: 'detail', meta: {name: '详情'}, component: Detail},
    {path: "/setting/:tab", name: "setting", meta: {name: '设置'}, component: Setting}
];
export default new Router({
    mode: "history",
    routes
});
