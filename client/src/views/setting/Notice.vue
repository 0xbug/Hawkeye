<template>
    <div class="notice-setting">
        <el-row :gutter="10" class="dashboard">
            <el-col :xs="24" :sm="12" :md="12" :lg="4" :xl="4">
                <el-card shadow="hover">
                    <div :style="styles.dataItem" @click="MailDialogFormVisible=true">
                        <i class="iconfont icon-mail" :style="styles.dataItemImg"></i>
                        <div :style="styles.dataItemUnit">
                            <div :style="styles.unitAmount">邮件</div>
                            <div :style="styles.unitFooter">状态：<span
                                    :style="smtp_server.enabled?'color:#52c41a':'color:#f5222d'">{{smtp_server.enabled?'开启':'关闭'}}</span>
                            </div>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="4" :xl="4" v-for="webhook in webhooks">
                <el-card shadow="hover">
                    <i class="iconfont icon-trash" style="float: right;color: #868898"
                       v-on:click="delWebHookSetting(webhook.webhook)"></i>
                    <div :style="styles.dataItem" @click="WebHookDialogFormVisible=true;webhook_setting=webhook">
                        <i class="iconfont icon-dingtalk" :style="styles.dataItemImg"
                           v-if="webhook.webhook.indexOf('dingtalk')>-1"></i>
                        <i class="iconfont icon-wechat-fill" :style="styles.dataItemImg"
                           v-if="webhook.webhook.indexOf('weixin')>-1"></i>
                        <div :style="styles.dataItemUnit">
                            <div :style="styles.unitAmount" v-if="webhook.webhook.indexOf('dingtalk')>-1">钉钉</div>
                            <div :style="styles.unitAmount" v-if="webhook.webhook.indexOf('weixin')>-1">企业微信</div>
                            <div :style="styles.unitFooter">{{webhook.webhook.split('=')[1].slice(0,8)}}</div>
                            <div :style="styles.unitFooter">状态：<span
                                    :style="webhook.enabled?'color:#52c41a':'color:#f5222d'">{{webhook.enabled?'开启':'关闭'}}
                            </span>
                            </div>
                        </div>
                    </div>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="4" :xl="4">
                <el-card shadow="hover">
                    <div :style="styles.dataItem" @click="WebHookDialogFormVisible=true;webhook_setting={}">
                        <i class="iconfont icon-plus" :style="styles.dataItemImg"></i>
                        <div :style="styles.dataItemUnit">
                            <div :style="styles.unitAmountSmall">添加钉钉/微信告警</div>
                            <div :style="styles.unitFooter">oapi.dingtalk.com qyapi.weixin.qq.com</div>
                        </div>
                    </div>
                </el-card>
            </el-col>
        </el-row>
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
                    <el-input v-model="smtp_server.password" auto-complete="off" type="password"></el-input>
                </el-form-item>
                <el-form-item label="监控平台地址">
                    <el-input v-model="smtp_server.domain"
                              :placeholder="origin"></el-input>
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
        <el-dialog :visible.sync="WebHookDialogFormVisible" v-model="WebHookDialogFormVisible"
                   :width="mobileClient?'80%':'50%'">
            <div slot="title" :style="styles.unitAmountSmall">
                webhook 配置
                目前支持 钉钉/企业微信
            </div>

            <el-form :model="webhook_setting">

                <el-form-item label="webhook">
                    <el-input v-model="webhook_setting.webhook"
                              placeholder="https://oapi.dingtalk.com/robot/send?access_token=xxx 或 https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"></el-input>
                </el-form-item>
                <el-form-item label="监控平台地址">
                    <el-input v-model="webhook_setting.domain"
                              :placeholder="origin"></el-input>
                </el-form-item>
                <el-form-item label="开启通知">
                    <el-switch
                            v-model="webhook_setting.enabled"
                            active-color="#13ce66"
                            inactive-color="#ff4949">
                    </el-switch>
                </el-form-item>
                <el-form-item label="测试">
                    <el-button size="mini" round @click="testWebHookSetting"
                               :disabled="!webhook_setting.hasOwnProperty('webhook')">发送一条测试消息
                    </el-button>
                </el-form-item>

            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button size="mini" round @click="WebHookDialogFormVisible = false">取 消</el-button>
                <el-button size="mini" type="primary" round @click="setWebHookSetting">确 定</el-button>
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
            <el-button size="mini" type="primary" @click="handleInputNoticeConfirm">添加</el-button>
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
            width: "30px",
            marginTop: "auto",
            marginBottom: "auto",
            fontSize: "50px",
            marginRight: "30px"
        },
        dataItemUnit: {
            height: "50px",
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
        unitAmountSmall: {
            color: "#999",
            fontSize: "14px"
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
                origin: window.location.origin,
                inputValue: "",
                popoverVisible: false,
                MailDialogFormVisible: false,
                WebHookDialogFormVisible: false,
                mails: [],
                formLabelWidth: "200",
                smtp_server: {},
                webhook_setting: {domain: window.location.origin},
                webhooks: []
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
            getWebHookSetting() {
                this.axios
                    .get(this.api.settingWebHook)
                    .then(response => {
                        this.webhooks = response.data.result;

                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            delWebHookSetting(webhook) {
                this.axios
                    .delete(this.api.settingWebHook, {params: {webhook: webhook}})
                    .then(response => {
                        if (response.data.status === 404) {
                            this.$message.error(response.data.msg);

                        } else {
                            this.$message.success(response.data.msg);
                            this.getWebHookSetting()

                        }

                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            setWebHookSetting() {
                this.axios
                    .post(this.api.settingWebHook, this.webhook_setting)
                    .then(response => {
                        if (response.data.status === 400) {
                            this.$message.error(response.data.msg);

                        } else {
                            this.$message.success(response.data.msg);
                            this.WebHookDialogFormVisible = false;
                            this.getWebHookSetting()
                        }
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            testWebHookSetting() {
                this.webhook_setting.test = true;
                this.axios
                    .post(this.api.settingWebHook, this.webhook_setting)
                    .then(response => {
                        if (response.data.status === 201) {
                            this.$message.success(response.data.msg);
                        } else {
                            this.$message.error(response.data.msg);
                        }
                        this.webhook_setting.test = false;

                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                        this.webhook_setting.test = false;

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
            this.getWebHookSetting();
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