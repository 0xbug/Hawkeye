<template>
    <el-row :gutter="10">
        <el-col :xs="24" :sm="24" :md="24" :lg="12" :xl="12">
            <el-card class="card-panel" shadow="never">
                <div style="min-height: 250px">
                    <el-form :model="form">
                        <el-form-item label="GitHub用户">
                            <img class="avatar" :src="leakageInfo.avatar_url" width="32"
                                 height="32"
                                 :alt="'@'+leakageInfo.username">
                        </el-form-item>
                        <el-form-item label="仓库地址">
                            <a :href="leakageInfo.project_url" target="_blank"
                               referrerpolicy="no-referrer">{{leakageInfo.project}}</a>
                            –
                            <a :href="leakageInfo.link" target="_blank" referrerpolicy="no-referrer">{{leakageInfo.filename}}</a>
                        </el-form-item>
                        <el-form-item label="仓库信息">
                            <div class="project-info">
                                <img :src="'https://img.shields.io/github/issues/'+leakageInfo.project+'.svg?longCache=true&style=flat'"
                                     alt="">
                                <img :src="'https://img.shields.io/github/forks/'+leakageInfo.project+'.svg?longCache=true&style=flat'"
                                     alt="">
                                <img :src="'https://img.shields.io/github/stars/'+leakageInfo.project+'.svg?longCache=true&style=flat'"
                                     alt="">
                            </div>
                        </el-form-item>
                        <el-form-item label="编码语言">
                            {{leakageInfo.language}}
                        </el-form-item>
                        <el-form-item label="上传时间">
                            {{leakageInfo.datetime|dateFormat}}
                        </el-form-item>
                        <el-form-item label="命中标签">
                            <el-tag size="mini" type="danger">
                                <router-link :to="{name:'index',query:{tag:leakageInfo.tag}}">{{leakageInfo.tag}}
                                </router-link>
                            </el-tag>
                        </el-form-item>
                    </el-form>
                </div>
            </el-card>
        </el-col>
        <el-col :xs="24" :sm="24" :md="24" :lg="12" :xl="12">
            <el-card class="card-panel" shadow="never">
                <div style="min-height: 260px">
                    <el-form :model="form">

                        <el-form-item label="是否安全">
                            <el-radio-group v-model="form.security">

                                <el-radio :label="1">安全</el-radio>
                                <el-radio :label="0">涉密</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="忽略仓库">
                            <el-radio-group v-model="form.ignore">

                                <el-radio :label="1">忽略</el-radio>
                                <el-radio :label="0">监控</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="备注">

                            <el-input v-model="form.desc" type="textarea" placeholder="请输入..." :rows="3"></el-input>

                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" round size="mini" @click="dealLeakage">确认</el-button>
                            <el-button type="primary" round size="mini" @click="quickCheck(leakageInfo)">快速排查
                            </el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </el-card>
        </el-col>
        <el-col :span="24" v-if="code">
            <div class="card">
                <el-collapse>
                    <el-collapse-item :title="'受影响资产 ('+affect.length+'个)'" name="affect">
                        <el-table
                                :data="affect"
                                fit
                                style="width: 100%">
                            <el-table-column
                                    prop="type"
                                    label="泄露类型"
                            >
                            </el-table-column>
                            <el-table-column
                                    prop="value"
                                    label="受影响资产"
                            >
                            </el-table-column>
                        </el-table>
                    </el-collapse-item>

                </el-collapse>
            </div>
            <el-card shadow="never">
                <div class="clearfix" slot="header">
                    <i class="el-icon-document" style="margin-right: 4px;"></i>
                    <a :href="leakageInfo.link" target="_blank">可疑文件</a>
                </div>
                <highlight-code lang="python">
                    {{code}}
                </highlight-code>

            </el-card>
        </el-col>
    </el-row>
</template>
<script>
    import {Base64} from "js-base64";
    import "highlight.js/styles/github.css";

    export default {
        data() {
            return {
                leakageInfo: {},
                code: "",
                affect: null,
                form: {security: 1, ignore: 1, desc: ""}
            };
        },
        computed: {
            leakageID() {
                return this.$route.params.id;
            }
        },

        methods: {
            quickCheck(leakageInfo) {
                const url =
                    leakageInfo.project_url +
                    "/search?utf8=✓&q=pass OR password OR passwd OR pwd OR smtp OR database";
                window.open(url, "_blank");
            },
            fetchInfoData() {
                this.axios
                    .get(this.api.leakageInfo, {
                        params: {
                            id: this.leakageID
                        }
                    })
                    .then(response => {
                        this.leakageInfo = response.data.result;
                        this.form.security = this.leakageInfo.security;
                        this.form.project = this.leakageInfo.project;
                        this.form.ignore = this.leakageInfo.ignore;
                        this.form.desc = this.leakageInfo.desc;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            fetchCodeData() {
                this.axios
                    .get(this.api.leakageCode, {
                        params: {
                            id: this.leakageID
                        }
                    })
                    .then(response => {
                        this.code = Base64.decode(response.data.result.code);
                        this.affect = response.data.result.affect;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            dealLeakage() {
                this.form.id = this.$route.params.id;
                this.axios
                    .patch(this.api.leakage, this.form)
                    .then(response => {
                        this.$message.success(response.data.msg);
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            }
        },
        mounted() {
            this.fetchInfoData();
            this.fetchCodeData();
            this.$nextTick(function () {
            });
        }
    };
</script>

<style>
    .project-info img {
        margin-right: 5px;
    }

    .card {
        background-color: #ffffff;
        padding: 10px 10px 10px 30px;
        border: 1px solid #ebeef5;
        border-radius: 4px;
        margin-bottom: 5px;
    }

    .el-tag--danger a {
        color: #f56c6c !important;
    }
</style>
