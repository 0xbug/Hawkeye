<template>
    <div class="navigation">
        <el-menu
                background-color="#24292e"
                text-color="rgba(255, 255, 255, 0.75)"
                active-text-color="#fff"
                :default-active="activeIndex"
                router
                mode="horizontal">
            <el-menu-item index="" disabled>
                <img src="./../assets/github.svg" style="font-size: 20px;width: 3em;height: 1.5em;" alt="">
                GitHub 监控平台
            </el-menu-item>
            <el-menu-item index="/">
                概览
            </el-menu-item>
            <el-menu-item index="/setting/rule">
                配置
            </el-menu-item>

        </el-menu>
    </div>
</template>


<script>
    export default {
        data() {
            return {};
        },
        computed: {
            activeIndex() {
                return this.$route.name;
            }
        },
        mounted: function () {
            this.$nextTick(function () {
            });
        }
    };
</script>

<style>
    .el-menu-item a {
        text-decoration: none;
        display: block;
    }
</style>
