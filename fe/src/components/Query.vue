<template>
  <div class="setting-card">
    <el-card>
      <div slot="header">
        <span class="tip"><i class="el-icon-information"></i>
          <a rel="noopener noreferrer"
             href="https://github.com/search/advanced"
             target="_blank">搜索语法</a>
        </span>
        <el-button style="float: right;" type="info" @click="dialogFormVisible = true">
          <i class="el-icon-plus"></i>
        </el-button>
        <el-dialog title="添加" v-model="dialogFormVisible">
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

          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">取 消</el-button>
            <el-button type="primary" @click="handleAddQuery(form)">确 定</el-button>
          </div>
        </el-dialog>
      </div>

      <el-table
        :data="querys"
        style="width: 100%"
        :border="true"
        :stripe="true"

      >
        <el-table-column
          label="名称"
        >
          <template scope="scope">
            <span style="margin-left: 10px">
              <router-link :to="'/view/tag/'+scope.row.tag">
                {{scope.row.tag}}
              </router-link>
            </span>
          </template>
        </el-table-column>
        <el-table-column
          label="关键字"
        >
          <template scope="scope">
            <span style="margin-left: 10px"><a
              rel="noopener noreferrer"
              :href="'https://github.com/search?o=desc&q='+scope.row.keyword+'&ref=searchresults&s=indexed&type=Code&utf8=%E2%9C%93'"
              target="_blank">{{scope.row.keyword}}</a></span>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
        >
          <template scope="scope">
            <el-button
              size="small"
              @click="handleEdit(scope.$index, scope.row)">编辑
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDeleteQuery(scope.$index, scope.row)">删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>

</template>
<script>
  export default {
    data () {
      return {
        querys: [],
        dialogFormVisible: false,
        formLabelWidth: '120px',
        form: {
          'tag': '',
          'keyword': '',
        },
      }
    },
    methods: {
      handleEdit(index, row) {
        this.form = row;
        this.dialogFormVisible = true;
      },
      fetchQuery: function () {
        this.axios.get(this.GLOBAL.settingQuery)
          .then((response) => {
            this.querys = response.data.result;
          })
          .catch((error) => {
            this.$message.error(error.toString());
          });
      },
      handleDeleteQuery(index, row) {
        this.axios.delete(`${this.GLOBAL.settingQuery}?_id=${row._id}&tag=${row.tag}`)
          .then((response) => {
            this.$message.success(response.data.msg);
            this.dialogFormVisible = false;
            this.querys = response.data.result;
          })
          .catch((error) => {
            this.$message.error(error.toString());
            this.dialogFormVisible = false

          });
      }
      ,
      handleAddQuery(form) {
        this.axios.post(this.GLOBAL.settingQuery, form)
          .then((response) => {
            this.$message.success(response.data.msg);
            this.dialogFormVisible = false;
            this.querys = response.data.result;

          })
          .catch((error) => {
            this.$message.error(error.toString());
            this.dialogFormVisible = false

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
</script>
