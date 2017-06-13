<template>
  <div>

    <navmenu>
    </navmenu>
    <router-view></router-view>

  </div>
</template>

<script>
  import navmenu from '@/components/NavMenu';

  export default {
    name: 'app',
    components: {
      navmenu
    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }

  .el-card {
    margin-left: 5px;
    margin-right: 5px;
    margin-top: 10px;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    font-size: 14px;
    line-height: 1.5;
    color: #24292e;
    background-color: #fff;
  }
</style>
