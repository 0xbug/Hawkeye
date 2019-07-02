<template>
    <el-tabs
            v-model="activeName"
            type="border-card"
            lazy
            @tab-click="handleTabClick"
            :active-name="activeName">
        <el-tab-pane name="rule">
            <span slot="label"><i class="iconfont icon-search"></i>监控项</span>
            <Rule></Rule>
        </el-tab-pane>
        <el-tab-pane name="blacklist">
            <span slot="label"><i class="iconfont icon-shielding"></i>黑名单</span>
            <Blacklist></Blacklist>
        </el-tab-pane>
        <el-tab-pane name="notice">
            <span slot="label"><i class="iconfont icon-alert"></i>告警</span>
            <Notice></Notice>
        </el-tab-pane>
        <el-tab-pane name="task">
            <span slot="label"><i class="iconfont icon-task"></i>定时任务</span>
            <Task></Task>
        </el-tab-pane>
        <el-tab-pane name="github">
            <span slot="label"><i class="iconfont icon-github-fill"></i>GitHub账号</span>
            <Github></Github>
        </el-tab-pane>
    </el-tabs>
</template>
<script>
    const Notice = () => import("./Notice");
    const Github = () => import("./Github");
    const Rule = () => import("./Rule");
    const Task = () => import("./Task");
    const Blacklist = () => import("./Blacklist");

    export default {
        data() {
            return {
                activeName: this.$route.params.tab ? this.$route.params.tab : "rule"
            };
        },
        components: {
            Github,
            Notice,
            Blacklist,
            Task,
            Rule
        },
        methods: {
            handleTabClick(tab) {
                this.$router.push({name: "setting", params: {tab: tab.name}});
            }
        }
    };
</script>
<style>
    .el-tabs__nav-next, .el-tabs__nav-prev {
        margin-left: 5px;
        margin-right: 5px;
    }

    .tip a {
        text-decoration: none;
        line-height: 36px;
        color: #409eff;
    }

    .el-tab-pane {
        padding: 20px 5px 10px 5px;
    }

    .el-tabs--border-card {
        background: #fff;
        border: 1px solid #ebeef5;
        border-radius: 4px;
        -webkit-box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.12),
        0 0 6px 0 rgba(0, 0, 0, 0.04);
        box-shadow: none !important;
    }

    .el-tabs__nav i {
        margin-right: 5px;
    }
</style>
