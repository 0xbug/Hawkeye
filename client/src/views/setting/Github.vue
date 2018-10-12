<template>
    <div class="input-new-account">
        <el-form :inline="true" :model="formInline">
            <el-form-item label="账号">
                <el-input size="mini" v-model="formInline.username" placeholder="账号"></el-input>
            </el-form-item>
            <el-form-item label="密码">
                <el-input size="mini"
                          v-model="formInline.password" placeholder="密码"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button size="mini"
                           type="primary" @click="addGithubAccount">添加
                </el-button>
            </el-form-item>
        </el-form>
        <el-table
                stripe
                tooltip-effect="dark"
                :data="accounts"
                style="width: 100%"
        >
            <el-table-column
                    prop="username"
                    label="账号"
            >
            </el-table-column>
            <el-table-column
                    prop="mask_password"
                    label="密码"
            >
            </el-table-column>
            <el-table-column
                    prop="rate_limit"
                    label="配额剩余"
            >
                <template slot-scope="scope">
                    <el-tooltip effect="dark" :content="'剩余'+scope.row.rate_remaining" placement="top">
                        <el-progress :percentage="parseInt(scope.row.rate_remaining/scope.row.rate_limit*100)"></el-progress>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column
                    label="操作"
                    fixed="right"
            >
                <template slot-scope="scope">
                    <el-button size="mini" type="danger" round @click="deleteGithubAccount(scope.row)">删除
                    </el-button>

                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
    export default {
        name: "Github",
        data() {
            return {
                accounts: [],
                formInline: {}
            };
        },
        methods: {
            addGithubAccount() {
                if (
                    this.formInline.hasOwnProperty("password") ||
                    this.formInline.hasOwnProperty("username")
                ) {
                    this.axios
                        .post(this.api.settingGithub, this.formInline)
                        .then(response => {
                            if (response.data.status === 201) {
                                this.$message.success(response.data.msg);
                                this.accounts = response.data.result;
                            } else {
                                this.$message.error(response.data.msg);
                            }
                        })
                        .catch(error => {
                            this.$message.error(error.toString());
                        });
                } else {
                    this.$message.error("请输入用户名密码");
                }
            },
            deleteGithubAccount(item) {
                this.axios
                    .delete(this.api.settingGithub, {
                        params: {
                            username: item.username
                        }
                    })
                    .then(response => {
                        this.$message.success(response.data.msg);
                        this.accounts = response.data.result;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            fetchGithubAccount() {
                this.axios
                    .get(this.api.settingGithub)
                    .then(response => {
                        this.accounts = response.data.result;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            }
        },
        created() {
            this.fetchGithubAccount();
        }
    };
</script>
