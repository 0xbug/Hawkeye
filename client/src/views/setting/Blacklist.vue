<template>
    <div class="blacklists">
        <el-alert
                title="项目名称、文件名若包含黑名单关键字，则不会保存。"
                type="warning"
                :closable="false"
                show-icon>
        </el-alert>

        <el-input
                class="input-new-blacklist"
                v-model="inputValue"
                size="mini"
                @keyup.enter.native="addBlacklist"
                @blur="addBlacklist"
        >
        </el-input>
        <el-button size="mini" type="primary" @click="addBlacklist">添加</el-button>
        <el-table stripe
                  tooltip-effect="dark"
                  :data="blacklists"
                  style="width: 100%">
            <el-table-column
                    prop="text"
                    label="关键字"
            >
            </el-table-column>
            <el-table-column
                    label="操作"
                    fixed="right"
            >
                <template slot-scope="scope">
                    <el-button size="mini" type="danger" round @click="deleteBlacklist(scope.row)">删除
                    </el-button>

                </template>
            </el-table-column>
        </el-table>

    </div>


</template>
<script>
    export default {
        data() {
            return {
                blacklists: [],
                enable: false,
                inputValue: ""
            };
        },
        methods: {
            addBlacklist() {
                if (this.inputValue) {
                    this.blacklists.push({text: this.inputValue});
                    this.axios
                        .post(this.api.settingBlacklist, {text: this.inputValue})
                        .then(response => {
                            this.$message.success(response.data.msg);
                            this.blacklists = response.data.result;
                        })
                        .catch(error => {
                            this.$message.error(error.toString());
                        });
                }
                this.inputValue = "";
            },

            deleteBlacklist(item) {
                this.axios
                    .delete(this.api.settingBlacklist, {
                        params: {
                            text: item.text
                        }
                    })
                    .then(response => {
                        this.$message.success(response.data.msg);
                        this.blacklists.splice(this.blacklists.indexOf(item), 1);
                        this.blacklists = response.data.result;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            fetchBlacklists() {
                this.axios
                    .get(this.api.settingBlacklist)
                    .then(response => {
                        this.blacklists = response.data.result;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            }
        },
        mounted: function () {
            this.fetchBlacklists();
        }
    };
</script>

<style scoped>
    .input-new-blacklist {
        margin-right: 10px;
        width: 233px;
        margin-top: 15px;
        vertical-align: bottom;
    }

    .input-new-blacklist .el-input__inner {
        height: 25px;
    }
</style>
