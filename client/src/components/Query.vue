<template>
  <div class="setting-card">
    <el-card shadow="never">
      <div slot="header">
        <span class="tip">
           <svg class="icon" aria-hidden="true" style="font-size: 20px">
              <use xlink:href="#icon-tip"></use>
            </svg>
                <a rel="noopener noreferrer"
                   href="https://github.com/search/advanced"
                   target="_blank">搜索语法</a>
              </span>
        <el-button style="float: right;" type="info" @click="dialogFormVisible = true">
          <i class="el-icon-plus"></i>
        </el-button>
        <el-dialog title="添加" :visible.sync="dialogFormVisible" v-model="dialogFormVisible">
          <el-form :model="form">
            <el-tooltip content="若存在，会覆盖已有值" placement="right">
              <el-form-item label="名称" :label-width="formLabelWidth">
                <el-input v-model="form.tag" auto-complete="off"></el-input>
              </el-form-item>
            </el-tooltip>
            <el-tooltip content="熟悉搜索语法可以提高监控效率: OR/AND/NOT" placement="right">
              <el-form-item label="关键字" :label-width="formLabelWidth">
                <el-input v-model="form.keyword" auto-complete="off"></el-input>
              </el-form-item>
            </el-tooltip>
            <el-form-item label="开启/关闭" :label-width="formLabelWidth">

              <el-switch
                v-model="form.enabled"
                active-color="#13ce66"
                inactive-color="#ff4949">
              </el-switch>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="handleAddQuery(form)">确 定</el-button>
          </div>
        </el-dialog>
      </div>

      <el-table :data="querys" :stripe="true">
        <el-table-column label="名称">
          <template slot-scope="scope">
            <router-link :to="'/view/tag/'+scope.row.tag">
              {{scope.row.tag}}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column
          label="状态"
          width=100
          prop="enabled"
          sortable
        >
          <template slot-scope="scope">
            <el-switch
              @change="updateEnabled(scope.row)"
              v-model="scope.row.enabled"
              active-color="#13ce66"
              inactive-color="#ff4949">
            </el-switch>
          </template>
        </el-table-column>
        <el-table-column
          label="关键字"
          width=400
          show-overflow-tooltip
        >
          <template slot-scope="scope">
            <a
              rel="noopener noreferrer"
              :href="'https://github.com/search?o=desc&q='+scope.row.keyword+'&ref=searchresults&s=indexed&type=Code&utf8=%E2%9C%93'"
              target="_blank">{{scope.row.keyword}}</a>
          </template>
        </el-table-column>
        <el-table-column
          label="最后抓取时间"
          prop="last"
          width=150
          sortable

        >
          <template slot-scope="scope">

            <span v-if="scope.row.last">{{ scope.row.last * 1000|timeago }}</span>
          </template>
        </el-table-column>


        <el-table-column
          label="操作"
          fixed="right"
          width=200

        >

          <template slot-scope="scope">

            <el-button-group>

              <el-button
                size="mini"
                plain
                @click="handleEdit(scope.$index, scope.row)">编辑
              </el-button>
              <el-button
                size="mini"
                type="danger"
                plain
                @click="handleDeleteQuery(scope.$index, scope.row)">删除
              </el-button>
              <el-button v-if="scope.row.status===0" size="mini"
                         plain
                         type="primary"
                         icon="el-icon-loading" @click="handleSpiderResult(scope.row)"></el-button>
              <el-button v-if="scope.row.status===1" size="mini" type="success"
                         plain
                         icon="el-icon-success" @click="handleSpiderResult(scope.row)"></el-button>
              <el-button v-if="scope.row.status===-1" size="mini" type="warning"
                         plain
                         icon="el-icon-warning" @click="handleSpiderResult(scope.row)"></el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>

</template>

<script>
  import Timeago from "timeago.js";

  const timeagoInstance = new Timeago();
  export default {
    data() {
      return {
        querys: [],
        dialogFormVisible: false,
        formLabelWidth: "120px",
        form: {
          tag: "",
          keyword: "",
          enabled: true
        }
      };
    },
    filters: {
      timeago(val) {
        return timeagoInstance.format(val, 'zh_CN')
      }
    },
    methods: {
      handleEdit(index, row) {
        this.form = row;
        this.dialogFormVisible = true;
      },
      fetchQuery: function () {
        this.axios
          .get(this.GLOBAL.settingQuery)
          .then(response => {
            this.querys = response.data.result;
          })
          .catch(error => {
            this.$message.error(error.toString());
          });
      },
      handleSpiderResult(result) {
        const last = timeagoInstance.format(result.last * 1000, "zh_CN");
        if (result.status > -1) {
          this.$message.success(last + result.reason);
        } else {
          this.$message.warning(last + result.reason);
        }
      },
      handleDeleteQuery(index, row) {
        this.axios
          .delete(`${this.GLOBAL.settingQuery}?_id=${row._id}&tag=${row.tag}`)
          .then(response => {
            this.$message.success(response.data.msg);
            this.dialogFormVisible = false;
            this.querys = response.data.result;
          })
          .catch(error => {
            this.$message.error(error.toString());
            this.dialogFormVisible = false;
          });
      },
      updateEnabled(row) {
        const params = {
          tag: row.tag,
          keyword: row.keyword,
          enabled: row.enabled
        };
        this.axios
          .post(this.GLOBAL.settingQuery, params)
          .then(response => {
            this.$message.success(response.data.msg);
            this.dialogFormVisible = false;
            this.querys = response.data.result;
          })
          .catch(error => {
            this.$message.error(error.toString());
            this.dialogFormVisible = false;
          });
      },
      handleAddQuery(form) {
        this.axios
          .post(this.GLOBAL.settingQuery, form)
          .then(response => {
            this.$message.success(response.data.msg);
            this.dialogFormVisible = false;
            this.querys = response.data.result;
          })
          .catch(error => {
            this.$message.error(error.toString());
            this.dialogFormVisible = false;
          });
      }
    }
    ,
    mounted: function () {
      this.fetchQuery();
      this.$nextTick(function () {
      });
    }
  }
  ;
</script>
