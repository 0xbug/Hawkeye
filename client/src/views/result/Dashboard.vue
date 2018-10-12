<template>
    <el-row :gutter="10" class="dashboard" v-if="trend.hasOwnProperty('all')">
        <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
            <el-card shadow="hover">
                <div :style="styles.dataItem">
                    <i class="iconfont icon-github-fill" :style="styles.dataItemImg"></i>
                    <div :style="styles.dataItemUnit">
                        <div :style="styles.dataTitle">泄露总数(个)</div>
                        <div :style="styles.dataAmount">{{trend.all.total}}</div>
                        <div :style="styles.dataFooter">今日：<span :style="trend.today.total?'color:#f5222d':''">{{trend.today.total}}</span></div>
                    </div>
                </div>
            </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
            <el-card shadow="hover">
                <div :style="styles.dataItem">
                    <i class="iconfont icon-alert" :style="styles.dataItemImg"></i>
                    <div :style="styles.dataItemUnit">
                        <div :style="styles.dataTitle">已确认(个)</div>
                        <div :style="styles.dataAmount">{{trend.all.risk}}</div>
                        <div :style="styles.dataFooter">今日：<span :style="trend.today.risk?'color:#f5222d':''">{{trend.today.risk}}</span> </div>
                    </div>
                </div>
            </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
            <el-card shadow="hover">
                <div :style="styles.dataItem">
                    <i class="iconfont icon-empty" :style="styles.dataItemImg"></i>
                    <div :style="styles.dataItemUnit">
                        <div :style="styles.dataTitle">已忽略(个)</div>
                        <div :style="styles.dataAmount">{{trend.all.ignore}}</div>
                        <div :style="styles.dataFooter">今日：{{trend.today.ignore}}</div>
                    </div>
                </div>
            </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="12" :lg="6" :xl="6">
            <el-card shadow="hover">
                <div :style="styles.dataItem">
                    <i class="iconfont icon-api" :style="styles.dataItemImg"></i>
                    <div :style="styles.dataItemUnit">
                        <div :style="styles.dataTitle">查询引擎</div>
                        <div :style="styles.dataAmount">{{trend.engine.status?'正常':'离线'}}</div>
                        <div :style="styles.dataFooter">最近：{{trend.engine.last*1000|timeAgo}}</div>
                    </div>
                </div>
            </el-card>
        </el-col>
    </el-row>
</template>

<script>
    const styles = {
        dataItem: {
            display: "flex",
            flexBasis: "50%",
            alignItems: "center"
        },
        dataItemImg: {
            color: "#1890ff",
            marginTop: "auto",
            marginBottom: "auto",
            fontSize: "60px",
            marginRight: "30px"
        },
        dataItemUnit: {
            height: "60px",
            display: "flex",
            flexBasis: "50%",
            flexDirection: "column",
            justifyContent: "space-between"
        },
        dataTitle: {
            color: "#666",
            fontSize: "12px"
        },
        dataAmount: {
            color: "#333",
            fontSize: "24px"
        },
        dataFooter: {
            color: "#999",
            fontSize: "12px"
        }
    };
    export default {
        name: "Dashboard",
        props: ["trend"],
        data() {
            return {
                styles
            };
        }
    };
</script>

<style lang="scss">
    .dashboard {
        margin-bottom: 10px;
        .el-card {
            margin-bottom: 5px;
        }
        .dashboard-icon {
            width: 60px;
            height: 60px;
            background-color: #1890ff;
            border-radius: 60px;
            i {
                font-size: 60px;
                text-align: center;
                color: #ffffff;
            }
        }
    }
</style>
