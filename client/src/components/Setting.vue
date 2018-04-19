<template>
  <el-card shadow="never">
    <el-tabs
      type="border-card"
      tab-position="left"
      active-name="query">
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
  </el-card>
</template>
<script>
  const Notice = () => import ('./Notice');
  const Query = () => import ('./Query');
  const Cron = () => import ('./Cron');
  const Blacklist = () => import ('./Blacklist');

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
    color: #409EFF;
  }

  .item {
    padding: 5px 0;
    margin-left: 10px;
    margin-right: 10px;
  }

  .item .el-tag {
    margin-top: 5px;
    margin-left: 5px;
    margin-right: 5px;
  }

  .el-tabs--border-card {
    margin-top: 5px;
    margin-left: 10px;
    margin-right: 10px;
    background: #fff;
    border: 0 !important;
    /*-webkit-box-shadow: 0 2px 4px 0 rgba(0,0,0,.12), 0 0 6px 0 rgba(0,0,0,.04);*/
    box-shadow: none !important;
  }
</style>
