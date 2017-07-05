<template>
  <el-tabs active-name="query">
    <el-tab-pane name="query">
      <span slot="label"><i class="el-icon-edit"></i> 关键词配置</span>
      <Query></Query>
    </el-tab-pane>

    <el-tab-pane name="blacklist">
      <span slot="label"><i class="el-icon-menu"></i> 黑名单</span>
      <Blacklist></Blacklist>

    </el-tab-pane>
    <el-tab-pane name="notice">
      <span slot="label"><i class="el-icon-message"></i> 告警管理</span>
      <Notice></Notice>

    </el-tab-pane>

    <el-tab-pane name="cron">
      <span slot="label"><i class="el-icon-date"></i> 定时任务配置</span>
      <Cron></Cron>


    </el-tab-pane>
  </el-tabs>

</template>
<script>
  import Notice from './Notice';
  import Query from './Query';
  import Cron from './Cron';
  import Blacklist from './Blacklist';

  export default {
    components: {
      Notice,
      Blacklist,
      Cron,
      Query
    }

  }
</script>
<style>
  .tip a {
    text-decoration: none;
    line-height: 36px;
  }

  .item {
    padding: 5px 0;
    margin-left: 10px;
    margin-right: 10px;
  }

  .item .el-tag {
    margin-top: 5px;
    margin-left: 10px;
    margin-right: 10px;
  }
</style>
