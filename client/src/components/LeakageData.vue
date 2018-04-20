<template>
  <div>
    <el-row :gutter="8">
      <el-col :md="24" :lg="24">
        <el-card shadow="never">
          <div slot="header">
            <el-select v-model="filters.tag"
                       size="small"
                       filterable
                       clearable
                       placeholder="请选择关键字"
                       @change="handleFilter"
                       @focus="fetchStatisticsData('tag')"
            >
              <el-option
                v-for="item in statistics.tag"
                :key="item._id"
                :value="item._id">
                {{item._id}} <span class="tag-count">{{item.value}}</span>
              </el-option>
            </el-select>
            <el-select v-model="filters.language"
                       size="small"
                       filterable
                       clearable
                       placeholder="请选择语言"
                       @change="handleFilter"
                       @focus="fetchStatisticsData('language')"
            >
              <el-option
                v-for="item in statistics.language"
                :key="item._id"
                :value="item._id">
                {{item._id}} <span class="tag-count">{{item.value}}</span>
              </el-option>
            </el-select>
            <el-radio-group v-model="filters.status" @change="handleFilter" size="small">
              <el-radio-button :label="{}">不限</el-radio-button>
              <el-radio-button :label="{security: 0,desc: {
                          $exists: false}}">
                <i class="el-icon-time"></i> 待处理
              </el-radio-button>
              <el-radio-button :label="{security: 0, desc: {
                          $exists: true}}">
                <i class="el-icon-star-on"></i> 已处理
              </el-radio-button>
              <el-radio-button :label="{security: 1}">
                <i class="el-icon-check"></i> 归档
              </el-radio-button>
            </el-radio-group>
            <div class="page-top" v-if="leakagesData">
              <el-pagination small @size-change="handleSizeChange" @current-change="handleCurrentChange"
                             :current-page="from" :page-sizes="[20, 50,100]" :page-size="limit"
                             layout="total,prev, pager, next, sizes" :total="total">
              </el-pagination>

            </div>
          </div>
          <SearchResults :results="leakagesData"></SearchResults>
          <div class="page" v-if="leakagesData">
            <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange"
                           :current-page="from" :page-sizes="[20, 50,100]" :page-size="limit"
                           layout="prev, pager, next, jumper" :total="total">
            </el-pagination>

          </div>
        </el-card>
      </el-col>
    </el-row>

  </div>
</template>


<script>
  import Timeago from 'timeago.js';
  import {
    Base64
  } from 'js-base64';

  const timeagoInstance = new Timeago();
  const SearchResults = () => import("./SearchResults");

  export default {
    data() {
      return {
        statistics: {tag: [], language: []},
        filters: {
          status: {
            security: 0,
            desc: {
              $exists: false
            }
          },
          tag: this.$route.params.tag || ''
        },
        leakagesData: [],
        total: 10,
        limit: 10,
        from: 1
      }
    },
    methods: {
      handleFilter() {
        this.$router.push({name: 'tag', params: {tag: this.filters.tag}});
        this.from = 1;
        this.fetchLeakagesData();
      },
      fetchStatisticsData(by) {
        // if (this.statistics[by].length === 0) {
        this.axios.get(this.GLOBAL.statistics, {
          params: {
            by: by,
            tag: this.filters.tag
          }
        })
          .then((response) => {
            this.statistics[by] = response.data.result;

          })
          .catch((error) => {
            this.$message.error(error.toString());
          });
        // }
      },
      handleSizeChange(val) {
        this.limit = val;
        this.from = 1;
        this.fetchLeakagesData();
      },
      handleCurrentChange(val) {
        this.from = val;
        this.fetchLeakagesData();
      },
      handleTagSelected() {
        console.log(this.filters.tag);
        this.fetchLeakagesData()
      },
      fetchLeakagesData() {
        this.axios.get(this.GLOBAL.leakage, {
          params: {
            status: this.filters.status,
            tag: this.filters.tag,
            language: this.filters.language,
            limit: this.limit,
            from: this.from,
          }
        })
          .then((response) => {
            // this.$message.success(response.data.msg);
            this.leakagesData = response.data.result;
            this.total = response.data.total;

          })
          .catch((error) => {
            this.$message.error(error.toString());
          })
        ;
      }
    },
    components: {SearchResults},
    filters: {
      timeago(val) {
        return timeagoInstance.format(val, 'zh_CN')
      },
      b64decode(val) {
        return Base64.decode(val)
      },
    },
    mounted() {
      this.fetchLeakagesData();
      this.$nextTick(function () {

      });
    },
    watch: {
      '$route'(to, from) {
        this.filters.tag = to.params.tag || '';
        this.fetchLeakagesData();
      }
    }
  }
</script>
<style>
  @import "../style/github01.css";
  @import "../style/github02.css";
</style>
<style scoped>
  .code-list {
    margin-left: 200px;
  }

  .el-tag {
    border-radius: 2px !important;
    margin-right: 1px;
    font-weight: bold;
  }

  h3 {
    color: #313440;
  }

  p .icon {
    width: 1.2em;
    height: 1em;
    vertical-align: -0.15em;
    fill: currentColor;
    overflow: hidden;
  }

  p .icon-left {
    width: 1.2em;
    height: 1em;
    vertical-align: -0.15em;
    fill: currentColor;
    overflow: hidden;
  }

  .search-panel {
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .tag-count {
    float: right;
    color: #313440;
  }

  .page-top {
    float: right;
  }

  .search-result-tags .icon {
    width: 1.7em;
    height: 1.7em;
    vertical-align: -0.65em;
    fill: #F2F4F5;
    overflow: hidden;
  }
</style>
