<template>
    <div>
        <el-form :inline="false" label-width="150px">
            <el-form-item label="时间间隔（分钟）">
                <el-input-number v-model="minute"
                                 size="small"
                                 :max=30
                                 :min=5
                                 :step=1></el-input-number>
            </el-form-item>
            <el-form-item label="页数（30条/页）">
                <el-input-number v-model="page"
                                 size="small"
                                 :max=100
                                 :min=1
                                 :step=1
                ></el-input-number>
            </el-form-item>
        </el-form>
        <el-button type="primary" size="small" style="margin-left: 150px;width: 130px" @click="handleTaskSet">确认
        </el-button>

    </div>

</template>
<script>
    export default {
        data() {
            return {
                minute: 10,
                page: 1
            };
        },
        methods: {
            handleTaskSet() {
                this.axios
                    .post(this.api.settingCron, {
                        page: this.page,
                        minute: this.minute
                    })
                    .then(response => {
                        this.$message.success(response.data.msg);
                        this.fetchTaskSetting();
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            },
            fetchTaskSetting: function () {
                this.axios
                    .get(this.api.settingCron)
                    .then(response => {
                        if (response.data.status === 400) {
                            this.$message.error(response.data.msg);
                        } else {
                            this.page = response.data.result.page;
                            this.minute = response.data.result.minute;
                        }
                    })
                    .catch(error => {
                        this.$message.error(error.toString());
                    });
            }
        },
        mounted: function () {
            this.fetchTaskSetting();
        }
    };
</script>
