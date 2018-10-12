<template>
    <el-container>
        <el-header>
            <NavMenu>
            </NavMenu>
        </el-header>
        <div class="breadcrumb" v-if="$route.path!=='/'">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>{{$route.meta.name}}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <el-main>
            <router-view></router-view>
        </el-main>
        <el-footer>
            2016-{{year}} &copy; <a href="https://github.com/0xbug" target="_blank">0xbug</a>
        </el-footer>
    </el-container>
</template>

<script>
    const NavMenu = () => import("@/components/NavMenu");

    const date = new Date();
    const year = date.getFullYear();
    export default {
        name: "app",
        data() {
            return {
                year: year
            };
        },
        components: {
            NavMenu
        }
    };
</script>

<style>
    @import "./style/app.css";
    .el-main{
        min-height: 85vh;
    }
    .breadcrumb {
        padding: 20px 20px 20px 20px;
        background-color: #fff;
        /*margin-bottom: 5px;*/
    }
</style>
