<template>
  <div>
    <div v-if="results">
      <div class="search-result-item" :key="result._id" v-for="result in results">

        <el-card shadow="hover">
          <div class="search-result-item">
            <div class="code-list" id="codelist">
              <div v-html="result.detail">
              </div>
            </div>

          </div>

          <el-tag size="small">
            <router-link :to="'/view/tag/'+result.tag" target="_blank">
              {{result.tag}}
            </router-link>

          </el-tag>
          <el-tag type="danger" size="small" v-if="result.desc">
            {{result.desc|b64decode}}
          </el-tag>
          <el-button-group>
            <el-button round size="small">
              <router-link :to="'/view/leakage/'+result._id" target="_blank">
                详情
              </router-link>
            </el-button>
             <el-button round size="small">
              <a
                :href="'https://github.com/'+result.project+'/commits'"
                target="_blank"
                referrerpolicy="no-referrer"
              >
                Commits
              </a>
            </el-button>
            <el-button round size="small">
              <a
                :href="'https://github.com/'+result.project+'/search?utf8=✓&q=pass OR password OR passwd OR pwd OR smtp OR database'"
                target="_blank"
                referrerpolicy="no-referrer"
              >
                GitHub <i class="el-icon-search"></i>
              </a>
            </el-button>
          </el-button-group>
        </el-card>
      </div>
    </div>
    <div v-if="results.length===0">
      <img src="./../assets/no.png" width="500" height="300">
    </div>
  </div>

</template>

<script>
  import {
    Base64
  } from 'js-base64';

  export default {
    props: ['results'],
    name: "search-results",
    filters: {
      // timeago(val) {
      //   return timeagoInstance.format(val, 'zh_CN')
      // },
      b64decode(val) {
        return Base64.decode(val)
      },
    },
  }
</script>

<style scoped>

</style>
