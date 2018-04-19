<template>
  <div>
    <el-container>
      <el-header>
        <NavMenu>
        </NavMenu>
      </el-header>
      <el-main>
        <div class="card-panel-main">
          <router-view></router-view>
        </div>
      </el-main>
      <el-footer>
        2016-{{year}} &copy; <a href="https://github.com/0xbug" target="_blank">0xbug</a>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
  const NavMenu = () => import("@/components/NavMenu");

  const date = new Date;
  const year = date.getFullYear();
  export default {
    name: "app",
    data() {
      return {
        year: year
      }
    },
    components: {
      NavMenu
    }
  };
</script>

<style>
  @import "./style/app.css";
</style>
