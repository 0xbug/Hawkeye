<template>
    <div class="setting-card">
        <el-dialog title="添加监控项" :visible.sync="dialogFormVisible" v-model="dialogFormVisible"
                   :width="mobileClient?'80%':'50%'">
            <el-form :model="form">
                <el-form-item label="名称">
                    <el-popover
                            placement="right"
                            title="提示"
                            width="200"
                            trigger="hover"
                    >若存在相同名称，会覆盖已有值
                        <i class="el-icon-question" slot="reference"></i>
                    </el-popover>
                    <el-input v-model="form.tag" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="关键字">
                    <el-popover
                            placement="right"
                            title="提示"
                            width="200"
                            trigger="hover"
                    >熟悉
                        <a referrerpolicy="no-referrer"
                           href="https://github.com/search/advanced"
                           target="_blank">GitHub 搜索语法</a>可以提高监控效率: OR/AND/NOT
                        <i class="el-icon-question" slot="reference"></i>
                    </el-popover>
                    <el-input v-model="form.keyword" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="开启/关闭">

                    <el-switch
                            v-model="form.enabled"
                            active-color="#13ce66"
                            inactive-color="#ff4949">
                    </el-switch>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button round size="mini" @click="dialogFormVisible = false">取 消</el-button>
                <el-button round size="mini" type="primary" @click="handleAddQuery(form)">确 定</el-button>
            </div>
        </el-dialog>
        <el-button type="primary" size="mini" @click="dialogFormVisible = true">
            添加
        </el-button>
        <el-table :data="rules" :stripe="true">
            <el-table-column label="名称">
                <template slot-scope="scope">
                    <router-link :to="'/?tag='+scope.row.tag">
                        {{scope.row.tag}}
                    </router-link>
                </template>
            </el-table-column>

            <el-table-column
                    label="关键字"
                    show-overflow-tooltip
            >
                <template slot-scope="scope">
                    <a
                            rel="noopener noreferrer"
                            :href="'https://github.com/search?o=desc&q='+scope.row.keyword+'&ref=searchresults&s=indexed&type=Code&utf8=%E2%9C%93'"
                            target="_blank">{{scope.row.keyword}}</a>
                </template>
            </el-table-column>
            <el-table-column
                    label="最后抓取时间"
                    prop="last"
                    width=150
                    sortable

            >
                <template slot-scope="scope">

                    <span v-if="scope.row.last">{{ scope.row.last * 1000|timeAgo }}</span>
                </template>
            </el-table-column>
            <el-table-column
                    label="总数"
                    width=200
                    prop="api_total"
                    sortable
            >
            </el-table-column>
            <el-table-column
                    label="已抓取"
                    width=200
                    prop="found_total"
                    sortable
            >
            </el-table-column>
            <el-table-column
                    label="状态"
                    width=100
                    prop="enabled"
                    sortable
            >
                <template slot-scope="scope">
                    <el-switch
                            @change="updateEnabled(scope.row)"
                            v-model="scope.row.enabled"
                            active-color="#13ce66"
                            inactive-color="#ff4949">
                    </el-switch>
                </template>
            </el-table-column>

            <el-table-column
                    label="操作"
                    width=200
            >
                <template slot-scope="scope">

                    <el-button-group>

                        <el-button
                                size="mini"
                                plain
                                round
                                @click="handleEdit(scope.$index, scope.row)">编辑
                        </el-button>
                        <el-button
                                size="mini"
                                type="danger"
                                plain
                                @click="handleDeleteQuery(scope.$index, scope.row)">删除
                        </el-button>
                        <el-button v-if="scope.row.status===0" size="mini"
                                   plain
                                   round
                                   type="primary"
                                   icon="el-icon-loading" @click="handleSpiderResult(scope.row)"></el-button>
                        <el-button v-if="scope.row.status===1" size="mini" type="success"
                                   plain
                                   round
                                   icon="el-icon-success" @click="handleSpiderResult(scope.row)"></el-button>
                        <el-button v-if="scope.row.status===-1" size="mini" type="warning"
                                   plain
                                   round
                                   icon="el-icon-warning" @click="handleSpiderResult(scope.row)"></el-button>
                    </el-button-group>
                </template>
            </el-table-column>
        </el-table>
    </div>

</template>

<script>
    import {format} from "timeago.js";

    export default {
        data() {
            return {
                rules: [],
                dialogFormVisible: false,
                form: {
                    tag: "",
                    keyword: "",
                    enabled: true
                }
            };
        },
        computed: {
            mobileClient() {
                return document.documentElement.clientWidth < document.documentElement.clientHeight
            }
        },
        methods: {
            handleEdit(index, row) {
                this.form = row;
                this.dialogFormVisible = true;
            },
            fetchQuery: function () {
                this.axios
                    .get(this.api.settingQuery)
                    .then(response => {
                        this.rules = response.data.result;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            handleSpiderResult(result) {
                const last = format(result.last * 1000, "zh_CN");
                if (result.status > -1) {
                    this.$message.success(last + result.reason);
                } else {
                    this.$message.warning(last + result.reason);
                }
            },
            handleDeleteQuery(index, row) {
                this.axios
                    .delete(`${this.api.settingQuery}?_id=${row._id}&tag=${row.tag}`)
                    .then(response => {
                        this.$message.success(response.data.msg);
                        this.dialogFormVisible = false;
                        this.rules = response.data.result;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                        this.dialogFormVisible = false;
                    });
            },
            updateEnabled(row) {
                const params = {
                    tag: row.tag,
                    keyword: row.keyword,
                    enabled: row.enabled
                };
                this.axios
                    .post(this.api.settingQuery, params)
                    .then(response => {
                        this.$message.success(response.data.msg);
                        this.dialogFormVisible = false;
                        this.rules = response.data.result;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                        this.dialogFormVisible = false;
                    });
            },
            handleAddQuery(form) {
                this.axios
                    .post(this.api.settingQuery, form)
                    .then(response => {
                        this.$message.success(response.data.msg);
                        this.dialogFormVisible = false;
                        this.rules = response.data.result;
                        this.form = {
                            tag: "",
                            keyword: "",
                            enabled: true
                        };
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                        this.dialogFormVisible = false;
                    });
            }
        },
        mounted: function () {
            this.fetchQuery();
        }
    };
</script>
