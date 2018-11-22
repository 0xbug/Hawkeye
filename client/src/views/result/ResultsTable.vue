<template>
    <div>
        <el-row :gutter="10" class="ignore-btn">
            <el-col :span="2">
                <el-button
                        v-show="selections.length > 0"
                        @click="handleIgnore(selections.map(i => i._id))"
                        type="danger"
                        round
                        size="mini">忽略
                </el-button>
            </el-col>
        </el-row>
        <el-table
                stripe
                tooltip-effect="dark"
                ref="multipleTable"

                :data="results"
                style="width: 100%"
                @selection-change="handleSelectionChange"
        >
            <el-table-column
                    type="selection"
                    width="40">
            </el-table-column>
            <el-table-column
                    label="发现时间"
                    width="200"
            >
                <template slot-scope="scope">
                            <i class="iconfont icon-time_fill"></i>
                    {{scope.row.datetime|dateFormat}}
                </template>
            </el-table-column>

            <el-table-column
                    label="项目"
                    width="200"
                    show-overflow-tooltip
            >
                <template slot-scope="scope">
                    <img class="avatar flex-shrink-0 mr-2" :src="scope.row.avatar_url" width="32" height="32"
                         :alt="'@'+scope.row.username">
                    <a :href="scope.row.project_url" target="_blank"
                       class="link-gray-dark no-underline text-bold wb-break-all"> {{scope.row.project}}</a>
                </template>

            </el-table-column>
            <el-table-column
                    prop="language"
                    label="语言"
                    show-overflow-tooltip
            >
                <template slot-scope="scope">
                    <span class="repo-language-color ml-0" style="background-color:#555555;"></span>
                    {{scope.row.language?scope.row.language:'未知'}}
                </template>
            </el-table-column>
            <el-table-column
                    prop="filename"
                    label="文件名"
                    width="200"
                    show-overflow-tooltip
            >
                <template slot-scope="scope">
                    <router-link :to="'/view/leakage/'+scope.row._id" target="_blank">
                        {{scope.row.filename}} 
                    </router-link>

                </template>

            </el-table-column>
            <el-table-column
                    label="备注"
                    show-overflow-tooltip
            >
                <template slot-scope="scope" v-if="scope.row.desc">

                    <el-tag size="mini" :type="scope.row.security?'success':'danger'" disable-transitions>
                        {{scope.row.desc}}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column
                    label="标签"
                    width="100"
                    show-overflow-tooltip
            >
                <template slot-scope="scope">
                    <router-link :to="'/view/tag/'+scope.row.tag">
                        <el-tag size="mini">{{scope.row.tag}}</el-tag>
                    </router-link>
                </template>
            </el-table-column>
            <el-table-column
                    label="Star/Fork"
                    width="300"
            >
                <template slot-scope="scope">
                    <div class="project-info">
                        <img :src="'https://img.shields.io/github/issues/'+scope.row.project+'.svg'" alt="">
                        <img :src="'https://img.shields.io/github/forks/'+scope.row.project+'.svg'" alt="">
                        <img :src="'https://img.shields.io/github/stars/'+scope.row.project+'.svg'" alt="">
                    </div>

                </template>
            </el-table-column>
            <el-table-column
                    label="操作"
                    width="300"
            >
                <template slot-scope="scope">
                    <el-button-group>
                        <el-button round size="mini"
                                   v-on:click="handleOpen('https://github.com/'+scope.row.project+'/commits')">
                            <i class="iconfont icon-github-fill"></i>
                            Commits
                        </el-button>
                        <el-button round size="mini"
                                   v-on:click="handleOpen('https://github.com/'+scope.row.project+'/search?utf8=✓&q=pass OR password OR passwd OR pwd OR smtp OR database')">
                            <i class="iconfont icon-flashlight"></i>
                            快速排查
                        </el-button>
                    </el-button-group>
                </template>
            </el-table-column>
        </el-table>
    </div>

</template>

<script>
    export default {
        props: ["results"],
        name: "results-table",
        data() {
            return {
                selections: []
            };
        },
        methods: {
            handleOpen(href) {
                window.open(href, "_blank");
            },
            handleSelectionChange(val) {
                this.selections = val;
            },
            ignoreLeakage(id) {
                const form = {security: 1, ignore: 1, desc: "", id: id};
                this.axios
                    .patch(this.api.leakage, form)
                    .then(response => {
                        this.$emit('change')
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            handleIgnore(leakages) {
                this.$confirm("此操作将忽略结果, 是否继续?", "提示", {
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    type: "warning"
                })
                    .then(() => {
                        leakages.forEach(leakage => {
                            this.ignoreLeakage(leakage);
                        });
                        this.$message({
                            type: "success",
                            message: "处理成功"
                        });
                    })
                    .catch(() => {
                        this.$message({
                            type: "error",
                            message: "已取消"
                        });
                    });
            }
        }
    };
</script>
<style>
    .ignore-btn{
        margin-top: 10px

    }
    a {
        color: #0366d6;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    .repo-language-color {
        margin-right: 5px;
    }

    .search-result-item .el-card {
        padding-top: 20px !important;
    }

    .project-info img {
        margin-right: 2px;
    }
</style>
