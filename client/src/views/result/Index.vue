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
                            <el-radio-group v-model="filters.status" @change="handleFilter" size="mini" fill="#DDDDDD">
                                <el-radio-button :label="{}">
                                    <i class="iconfont icon-search"></i>不限
                                </el-radio-button>
                                <el-radio-button :label="{security: 0,desc: {
                          $exists: false}}">
                                    <i class="iconfont icon-feedback_fill"></i>待审
                                </el-radio-button>
                                <el-radio-button :label="{security: 0, desc: {
                          $exists: true}}">
                                    <i class="iconfont icon-flag_fill"></i>确认
                                </el-radio-button>
                                <el-radio-button :label="{security: 1}">
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
                    status: {
                        security: 0,
                        desc: {
                            $exists: false
                        }
                    },
                    tag: this.$route.params.tag || ""
                },
                trendData: {},
                leakagesData: [],
                total: 10,
                limit: 10,
                from: 1
            };
        },
        methods: {
            handleFilter() {
                this.$router.push({name: "tag", params: {tag: this.filters.tag}});
                this.from = 1;
                this.fetchLeakagesData();
                this.fetchTrend();
            },
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
            },
            handleSizeChange(val) {
                this.limit = val;
                this.from = 1;
                this.fetchLeakagesData();
            },
            handleCurrentChange(val) {
                this.from = val;
                this.fetchLeakagesData();
            },
            handleTagSelected() {
                this.fetchLeakagesData();
                this.fetchTrend();
            },
            handleChange(){
            this.fetchTrend();
            this.fetchLeakagesData();
            },
            fetchLeakagesData() {
                this.axios
                    .get(this.api.leakage, {
                        params: {
                            status: this.filters.status,
                            tag: this.filters.tag,
                            language: this.filters.language,
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
            },
            fetchTrend() {
                this.axios
                    .get(this.api.trend, {
                        params: {
                            tag: this.filters.tag
                        }
                    })
                    .then(response => {
                        this.trendData = response.data.result;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            }
        },
        components: {Dashboard, ResultsTable},
        computed: {
            mobileClient() {
                return document.documentElement.clientWidth < document.documentElement.clientHeight
            }
        },
        mounted() {
            this.fetchTrend();
            this.fetchLeakagesData();
        },
        watch: {
            $route(to, from) {
                this.filters.tag = to.params.tag || "";
                this.fetchLeakagesData();
                this.fetchTrend();
            }
        }
    };
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
