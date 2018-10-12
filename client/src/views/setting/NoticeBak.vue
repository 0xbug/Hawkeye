<template>
    <div class="notice-setting">
        <el-row :gutter="10" class="dashboard">
            <el-col :xs="24" :sm="12" :md="12" :lg="4" :xl="4">
                <el-card shadow="hover">
                    <div :style="styles.dataItem">
                        <i class="iconfont icon-mail" :style="styles.dataItemImg"></i>
                        <div :style="styles.dataItemUnit">
                            <div :style="styles.unitAmount">邮件</div>
                            <div :style="styles.unitFooter">状态：{{smtp_server.enabled?'开启':'关闭'}}</div>
                        </div>
                    </div>
                </el-card>
            </el-col>
        </el-row>
            <el-card shadow="never">

                <el-button size="mini" :type="smtp_server.enabled?'primary':'danger'" round
                           @click="MailDialogFormVisible=true">
                    <i class="iconfont icon-mail"></i>邮件配置
                </el-button>
                <el-button size="mini" :type="dingtalk.enabled?'primary':'danger'" round
                           @click="DingDialogFormVisible=true">
                    <i class="iconfont icon-dingtalk"></i>钉钉配置
                </el-button>
            </el-card>
            <el-dialog title="SMTP Server" :visible.sync="MailDialogFormVisible" v-model="MailDialogFormVisible"
                       :width="mobileClient?'80%':'50%'">
                <el-form :model="smtp_server">
                    <el-form-item label="服务器地址">
                        <el-input v-model="smtp_server.host" auto-complete="on"></el-input>
                    </el-form-item>
                    <el-form-item label="服务器端口">
                        <el-input-number v-model="smtp_server.port"
                                         size="small"
                                         controls-position="right"
                                         :max=65535
                                         :min=1
                                         :step=1
                        ></el-input-number>
                    </el-form-item>
                    <el-form-item label="发件人">
                        <el-input v-model="smtp_server.from" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="TLS加密">
                        <el-switch
                                v-model="smtp_server.tls"
                                active-color="#13ce66"
                                inactive-color="#ff4949">
                        </el-switch>
                    </el-form-item>
                    <el-form-item label="用户名">
                        <el-input v-model="smtp_server.username" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="密码">
                        <!--<el-input v-model="smtp_server.smtp_pass" auto-complete="off" type="password"></el-input>-->
                        <el-input v-model="smtp_server.password" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="开启通知">
                        <el-switch
                                v-model="smtp_server.enabled"
                                active-color="#13ce66"
                                inactive-color="#ff4949">
                        </el-switch>
                    </el-form-item>

                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button size="mini" round @click="MailDialogFormVisible = false">取 消</el-button>
                    <el-button size="mini" type="primary" round @click="setSMTPServer">确 定</el-button>
                </div>
            </el-dialog>
            <el-dialog title="钉钉配置" :visible.sync="DingDialogFormVisible" v-model="DingDialogFormVisible"
                       :width="mobileClient?'80%':'50%'">
                <el-form :model="dingtalk">
                    <el-form-item label="webhook">
                        <el-input v-model="dingtalk.webhook"
                                  placeholder="https://oapi.dingtalk.com/robot/send?access_token="></el-input>
                    </el-form-item>
                    <el-form-item label="开启通知">
                        <el-switch
                                v-model="dingtalk.enabled"
                                active-color="#13ce66"
                                inactive-color="#ff4949">
                        </el-switch>
                    </el-form-item>
                    <el-form-item label="测试">
                        <el-button size="mini" round @click="testDingTalk">发送一条测试消息</el-button>
                    </el-form-item>

                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button size="mini" round @click="DingDialogFormVisible = false">取 消</el-button>
                    <el-button size="mini" type="primary" round @click="setDingTalk">确 定</el-button>
                </div>
            </el-dialog>
            <div v-if="smtp_server.enabled">
                <el-input
                        class="input-new-mail"
                        v-model="inputValue"
                        size="mini"
                        placeholder="邮箱格式：username@domain.com"
                        @keyup.enter.native="handleInputNoticeConfirm"
                >
                </el-input>
                <el-button size="mini" type="primary" round @click="handleInputNoticeConfirm">添加</el-button>
                <el-table stripe
                          tooltip-effect="dark"
                          :data="mails"
                          style="width: 100%">
                    <el-table-column
                            prop="mail"
                            label="邮箱"
                    >
                    </el-table-column>
                    <el-table-column
                            label="操作"
                            fixed="right"
                    >
                        <template slot-scope="scope">
                            <el-button size="mini" type="danger" round @click="handleDeleteNotice(scope.row)">删除
                            </el-button>

                        </template>
                    </el-table-column>
                </el-table>
            </div>
    </div>
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
            width: "58px",
            height: "58px",
            fontSize: "58px",
            marginRight: "30px"
        },
        dataItemUnit: {
            height: "60px",
            display: "flex",
            flexBasis: "50%",
            flexDirection: "column",
            justifyContent: "space-between"
        },
        unitTitle: {
            color: "#666",
            fontSize: "12px"
        },
        unitAmount: {
            color: "#333",
            fontSize: "24px"
        },
        unitFooter: {
            color: "#999",
            fontSize: "12px"
        }
    };
    export default {
        data() {
            return {
                styles,
                inputValue: "",
                MailDialogFormVisible: false,
                DingDialogFormVisible: false,
                mails: [],
                formLabelWidth: "200",
                smtp_server: {},
                dingtalk: {}
            };
        },
        computed: {
            mobileClient() {
                return document.documentElement.clientWidth < document.documentElement.clientHeight
            }
        },
        methods: {
            handleInputNoticeConfirm() {
                if (this.inputValue) {
                    this.axios
                        .post(this.api.settingNotice, {mail: this.inputValue})
                        .then(response => {
                            this.$message.success(response.data.msg);
                            this.mails = response.data.result;
                        })
                        .catch(error => {
                            this.$message.error(error.toString());
                        });
                }
                this.inputValue = "";
            },

            handleDeleteNotice(mail) {
                this.axios
                    .delete(this.api.settingNotice, {
                        params: {
                            mail: mail.mail
                        }
                    })
                    .then(response => {
                        this.$message.success(response.data.msg);
                        this.mails = response.data.result;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            fetchNoticeMails() {
                this.axios
                    .get(this.api.settingNotice)
                    .then(response => {
                        this.mails = response.data.result;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            getSMTPServer() {
                console.log(this.smtp_server);
                this.axios
                    .get(this.api.settingMail)
                    .then(response => {
                        if (response.data.result) {
                            this.smtp_server = response.data.result;
                        }
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            getDingTalk() {
                this.axios
                    .get(this.api.settingDingTalk)
                    .then(response => {
                        if (response.data.result) {
                            this.dingtalk = response.data.result;
                        }
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            setDingTalk() {
                this.axios
                    .post(this.api.settingDingTalk, this.dingtalk)
                    .then(response => {
                        this.$message.success(response.data.msg);
                        this.DingDialogFormVisible = false;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            testDingTalk() {
                this.dingtalk.test = true;
                this.axios
                    .post(this.api.settingDingTalk, this.dingtalk)
                    .then(response => {
                        if (response.data.status === 201) {
                            this.$message.success(response.data.msg);
                        } else {
                            this.$message.error(response.data.msg);
                        }
                        this.dingtalk.test = false;

                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                        this.dingtalk.test = false;

                    });
            },
            setSMTPServer() {
                this.axios
                    .post(this.api.settingMail, this.smtp_server)
                    .then(response => {
                        this.$message.success(response.data.msg);
                        this.MailDialogFormVisible = false;
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            }
        },
        mounted: function () {
            this.getDingTalk();
            this.getSMTPServer();
            this.fetchNoticeMails();
        }
    };
</script>
<style scoped>
    .input-new-mail {
        margin-right: 10px;
        width: 233px;
        margin-top: 15px;
        vertical-align: bottom;
    }

    .input-new-mail .el-input__inner {
        height: 25px;
    }
</style>
