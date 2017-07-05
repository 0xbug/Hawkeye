<template>
  <div>
    <NavMenu>
    </NavMenu>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  import NavMenu from '@/components/NavMenu';

  export default {
    name: 'app',
    components: {
      NavMenu
    }
  }
</script>

<style>

  .content .el-card {
    margin-left: 5px;
    margin-right: 5px;
    margin-top: 10px;
    margin-bottom: 5px;
    border: 1px solid #fff;
    border-radius: 4px;
    background-color: #fff;
    overflow: hidden;
    box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .12), 0 0 6px 0 rgba(0, 0, 0, .04);
  }

  .el-card .el-card__header {
    padding: 10px 10px;
  }

  .el-card .el-card__body {
    padding: 10px;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    font-size: 14px;
    line-height: 1.5;
    color: #24292e;
    background-color: #fff;
  }

  body a {
    color: #0366d6;
    text-decoration: none;
    background-color: transparent;
  }
</style>
