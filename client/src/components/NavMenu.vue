<template>
  <div class="navigation">
    <el-menu
      background-color="rgb(36, 41, 46)"
      text-color="rgba(255, 255, 255, 0.75)"
      active-text-color="#fff"
      :default-active="activeIndex"
      router
      mode="horizontal">
      <el-menu-item index="" disabled>
        <svg class="icon" aria-hidden="true" style="font-size: 20px;width: 3em;
      height: 1.5em;">
          <use xlink:href="#icon-github"></use>
        </svg>
        GitHub 监控平台
      </el-menu-item>
      <el-menu-item index="/">
        概览
      </el-menu-item>
      <el-menu-item index="/setting">
        配置
      </el-menu-item>

    </el-menu>
  </div>
</template>


<script>
  export default {
    data() {
      return {
        activeIndex: '/',
      }
    },
    mounted: function () {
      this.$nextTick(function () {
      });
    }
  }
</script>

<style>
  .el-menu-item a {
    text-decoration: none;
    display: block;
  }
</style>
