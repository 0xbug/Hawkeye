<template>
  <div>

    <el-card shadow="never">
            <span slot="header">时间间隔          <el-button style="float:right" @click="handleCronSet">确认</el-button></span>
      <el-slider
        style="margin-left:20px"

        v-model="cron.every"
        :max=30
        :min=5
        :step=5
        show-stops
        show-input>
      </el-slider>
    </el-card>

    <el-card shadow="never">
        <span slot="header">
          爬取页数
                    <el-button style="float:right" @click="handleCronSet">确认</el-button>

        </span>

      <el-slider
        style="margin-left:20px"
        v-model="cron.page"
        :max=100
        :min=1
        :step=1
        show-input>

      </el-slider>


    </el-card>
  </div>

</template>
<script>
  export default {
    data() {
      return {
        cron: {every: 20, page: 1}
      };
    },
    methods: {
      handleCronSet() {
        this.axios
          .put(this.GLOBAL.settingCron, this.cron)
          .then(response => {
            this.$message.success(response.data.msg);
            this.fetchCron();
          })
          .catch(error => {
            this.$message.error(error.toString());
          });
      },
      fetchCron: function () {
        this.axios
          .get(this.GLOBAL.settingCron)
          .then(response => {
            this.cron = response.data.result;
          })
          .catch(error => {
            this.$message.error(error.toString());
          });
      }
    },
    mounted: function () {
      this.fetchCron();
      this.$nextTick(function () {
      });
    }
  };
</script>
<style>
  .el-card .el-card__header {
    padding: 10px 10px 20px
  }
</style>
