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
            <div slot="empty" style="margin: 20px">
                <img src="data:image/png;base64,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" alt="">
            </div>
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
                    width="100"
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
                    width="150"
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
                    <router-link :to="'/?tag='+scope.row.tag">
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
