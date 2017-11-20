<template>
  <div class="navigation">
    <el-menu 
    background-color="rgb(45, 47, 53)" 
    text-color="#fff"
    active-text-color="#0366d6"
    :default-active="activeIndex" mode="horizontal">
      <el-menu-item index="1">
        <router-link to="/">
          GitHub 监控平台
        </router-link>
      </el-menu-item>
      <el-submenu index="2">
        <template slot="title">
          <i class="el-icon-document"></i>概览
        </template>
        <el-menu-item :key="item._id" index="item._id" v-for="item in statistics">
          <router-link :to="{name: 'tag',params:{tag:item._id}}">
            {{item._id}}
            <el-badge :value=item.value></el-badge>
          </router-link>
        </el-menu-item>
      </el-submenu>

      <el-menu-item index="3">
        <router-link to="/setting">
          <i class="el-icon-setting"></i>配置
        </router-link>
      </el-menu-item>

    </el-menu>
  </div>
</template>


<script>
  export default {
    data() {
      return {
        activeIndex: '2',
        statistics: []
      }
    }, methods: {
      fetchStatisticsData() {
        this.axios.get(`${this.GLOBAL.statistics}`)
          .then((response) => {
            this.statistics = response.data.result;

          })
          .catch((error) => {
            this.$message.error(error.toString());
          });
      }
    },
    mounted: function () {
      this.fetchStatisticsData();
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
