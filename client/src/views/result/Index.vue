<template>
    <div class="result">
        <Dashboard :trend="trendData"></Dashboard>
        <el-card shadow="never">
            <el-form class="filter-panel">
                <el-row :type="mobileClient?'':'flex'">
                    <el-col :xs="24" :sm="24" :md="24" :lg="6" :xl="6">
                        <el-form-item label="标签">
                            <el-select v-model="filters.tag"
                                       size="small"
                                       filterable
                                       clearable
                                       placeholder="请选择关键字"
                                       @change="handleFilter"
                                       @focus="fetchStatisticsData('tag')"
                            >
                                <el-option
                                        v-for="item in statistics.tag"
                                        :key="item._id"
                                        :value="item._id">
                                    {{item._id}} <span class="tag-count">{{item.value}}</span>
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="6" :xl="6">
                        <el-form-item label="语言">
                            <el-select v-model="filters.language"
                                       size="small"
                                       filterable
                                       clearable
                                       placeholder="请选择语言"
                                       @change="handleFilter"
                                       @focus="fetchStatisticsData('language')"
                            >
                                <el-option
                                        v-for="item in statistics.language"
                                        :key="item._id"
                                        :value="item._id">
                                    {{item._id}} <span class="tag-count">{{item.value}}</span>
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :xs="24" :sm="24" :md="24" :lg="8" :xl="8">
                        <el-form-item label="状态">
                            <el-radio-group v-model="filters.status" @change="handleStatusFilter" size="mini"
                                            fill="#DDDDDD">
                                <el-radio-button label="不限">
                                    <i class="iconfont icon-search"></i>不限
                                </el-radio-button>
                                <el-radio-button label="待审">
                                    <i class="iconfont icon-feedback_fill"></i>待审
                                </el-radio-button>
                                <el-radio-button label="确认">
                                    <i class="iconfont icon-flag_fill"></i>确认
                                </el-radio-button>
                                <el-radio-button label="误报">
                                    <i class="iconfont icon-success_fill"></i>误报
                                </el-radio-button>
                            </el-radio-group>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <ResultsTable :results="leakagesData" @change="handleChange"></ResultsTable>
            <div class="page" v-if="leakagesData">
                <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                               :current-page="from" :page-sizes="[10, 20, 50,100]" :page-size="limit"
                               layout="total,prev, pager, next, sizes, jumper" :total="total">
                </el-pagination>

            </div>
        </el-card>

    </div>
</template>


<script>
    const Dashboard = () => import("./Dashboard");
    const ResultsTable = () => import("./ResultsTable");

    export default {
        data() {
            return {
                statistics: {tag: [], language: []},
                filters: {
                    status: this.$route.query.status || "待审",
                    tag: this.$route.query.tag || "",
                    language: this.$route.query.language || ""
                },
                trendData: {},
                leakagesData: [],
                total: 10
            };
        },
        computed: {
            mobileClient() {
                return document.documentElement.clientWidth < document.documentElement.clientHeight
            },
            status() {
                if (this.$route.query.status) {
                    if (this.$route.query.status === '不限') {
                        return {}
                    } else if (this.$route.query.status === '待审') {
                        return {
                            security: 0, desc: {
                                $exists: false
                            }
                        }
                    } else if (this.$route.query.status === '确认') {
                        return {
                            security: 0, desc: {
                                $exists: true
                            }
                        }
                    } else if (this.$route.query.status === '误报') {
                        return {security: 1}
                    }
                } else {
                    return {
                        security: 0,
                        desc: {
                            $exists: false
                        }
                    };
                }
            },
            from() {
                if (this.$route.query.page) {
                    return parseInt(this.$route.query.page, 10);
                } else {
                    return 1;
                }
            }
            ,
            tag() {
                if (this.$route.query.tag) {
                    return this.$route.query.tag;
                }
                if (this.$route.params.tag) {
                    return this.$route.params.tag;
                } else {
                    return "";
                }
            }
            ,
            language() {
                if (this.$route.query.language) {
                    return this.$route.query.language;
                } else {
                    return null;
                }
            }
            ,
            limit() {
                if (this.$route.query.limit) {
                    return parseInt(this.$route.query.limit, 10);
                } else {
                    return 10;
                }
            }
        },
        methods: {
            handleStatusFilter(status) {
                this.$router.push({
                    name: "index",
                    query: {page: 1, limit: 10, tag: this.filters.tag, language: this.filters.language, status: status}
                });
            }
            ,
            handleFilter() {
                this.$router.push({
                    name: "index",
                    query: {
                        page: 1,
                        limit: 10,
                        tag: this.filters.tag,
                        language: this.filters.language,
                        status: this.filters.status
                    }
                });
            }
            ,
            fetchStatisticsData(by) {
                this.axios
                    .get(this.api.statistic, {
                        params: {
                            by: by,
                            tag: this.filters.tag
                        }
                    })
                    .then(response => {
                        this.statistics[by] = response.data.result;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            }
            ,
            handleSizeChange(val) {
                this.$router.push({
                    name: "index",
                    query: {page: 1, limit: val, tag: this.tag, language: this.language, status: this.filters.status}
                });
            }
            ,
            handleCurrentChange(val) {
                this.$router.push({
                    name: "index",
                    query: {
                        page: val,
                        limit: this.limit,
                        tag: this.tag,
                        language: this.language,
                        status: this.filters.status
                    }
                });
            }
            ,
            handleChange() {
                this.fetchTrend();
                this.fetchLeakagesData();
            }
            ,
            fetchLeakagesData() {
                this.axios
                    .get(this.api.leakage, {
                        params: {
                            status: this.status,
                            tag: this.filters.tag,
                            language: this.language,
                            limit: this.limit,
                            from: this.from
                        }
                    })
                    .then(response => {
                        this.leakagesData = response.data.result;
                        this.total = response.data.total;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            }
            ,
            fetchTrend() {
                this.axios
                    .get(this.api.trend, {
                        params: {
                            tag: this.tag
                        }
                    })
                    .then(response => {
                        this.trendData = response.data.result;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            }
        }
        ,
        components: {
            Dashboard, ResultsTable
        }
        ,
        mounted() {
            this.fetchTrend();
            this.fetchLeakagesData();
        }
        ,
        watch: {
            $route(to, from) {
                this.filters.tag = to.query.tag || "";
                this.fetchLeakagesData();
                this.fetchTrend();
            }
        }
    }
    ;
</script>

<style scoped>
    .filter-panel {
        border-bottom: 1px dashed #e8e8e8;
    }

    .el-form-item__label {
        color: #313440;

    }

    .el-select {
        width: 233px;
    }

    .el-tag {
        border-radius: 2px !important;
        margin-right: 1px;
        font-weight: bold;
    }

    h3 {
        color: #313440;
    }

    .tag-count {
        float: right;
        color: #313440;
    }
</style>
