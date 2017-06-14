<template>
  <div>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="2">
          时间间隔
        </el-col>

        <el-col :span="14">
          <el-slider
            v-model="cron.every"
            :max=60
            :min=5
            :step=5
            show-stops
            show-input>
          </el-slider>
        </el-col>
        <el-col :span="8">
          <el-button @click="handleCronSet">确认</el-button>
        </el-col>
      </el-row>
    </el-card>
    <el-card>
      <el-row :gutter="20">
        <el-col :span="2">
          爬取页数
        </el-col>
        <el-col :span="14">
          <el-slider
            v-model="cron.page"
            :max=100
            :min=1
            :step=1
            show-input>

          </el-slider>
        </el-col>

        <el-col :span="8">
          <el-button @click="handleCronSet">确认</el-button>
        </el-col>
      </el-row>
    </el-card>
  </div>

</template>
<script>
  export default {
    data () {
      return {
        cron: {'every': 20, 'page': 1},

      }
    },
    methods: {
      handleCronSet(){
        this.axios.put(this.GLOBAL.settingCron, this.cron)
          .then((response) => {
              this.$message.success(response.data.msg);
              this.fetchCron();
            }
          ).catch((error) => {
          this.$message.error(error.toString());
        });
      },
      fetchCron: function () {
        this.axios.get(this.GLOBAL.settingCron)
          .then((response) => {
            this.cron = response.data.result;
          })
          .catch((error) => {
            this.$message.error(error.toString());
          });
      }

    }, mounted: function () {
      this.fetchCron();
      this.$nextTick(function () {
      });
    }
  }
</script>
