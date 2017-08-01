<template>
  <div>
    <el-card class="breadcrumb">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item :to="{path:`/view/tag/${leakageInfo.tag}`}">{{leakageInfo.tag}}</el-breadcrumb-item>
        <el-breadcrumb-item>{{leakageInfo.project}}</el-breadcrumb-item>
        <el-breadcrumb-item>{{leakageInfo.filename}}</el-breadcrumb-item>
      </el-breadcrumb>
    </el-card>
    <el-row :gutter="6">
      <el-col :xs="24" :sm="24" :md="16" :lg="16">
        <el-card>
  
          <div slot="header" class="clearfix">
            <span style="line-height: 36px;">
              <i class="el-icon-share" style="margin-right: 4px;"></i>
              <a :href="leakageInfo.link" target="_blank">可疑项目</a>
            </span>
            <a :href="'https://github.com/'+leakageInfo.project+'/search?utf8=✓&q=pass OR password OR passwd OR pwd OR smtp OR database'" target="_blank">
              <i class="el-icon-view" style="float: right;"></i>
  
            </a>
          </div>
  
          <div class="code-list" id="codelist">
            <div v-html="leakageInfo.detail"></div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="8" :lg="8">
        <el-card>
          <div style="padding: 5px;">
            <el-form :model="form">
              <el-form-item label="是否安全">
                <el-radio-group v-model="form.security">
  
                  <el-radio :label="1">安全</el-radio>
                  <el-radio :label="0">涉密</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="忽略仓库">
                <el-radio-group v-model="form.ignore">
  
                  <el-radio :label="1">忽略</el-radio>
                  <el-radio :label="0">监控</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="备注">
  
                <el-input v-model="form.desc" type="textarea" placeholder="请输入..."></el-input>
  
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="dealLeakage(form)">确认</el-button>
  
              </el-form-item>
            </el-form>
          </div>
        </el-card>
      </el-col>
      <el-col :span="24" v-if="code">
        <el-card>
          <div slot="header" class="clearfix">
            <span style="line-height: 36px;">
              <i class="el-icon-document" style="margin-right: 4px;"></i>
              <a :href="leakageInfo.link" target="_blank">可疑文件</a>
            </span>
          </div>
          <highlight-code :lang="leakageInfo.language">
            {{code}}
          </highlight-code>
  
        </el-card>
      </el-col>
    </el-row>
  
  </div>
</template>
<script>
import { Base64 } from 'js-base64';
import 'highlight.js/styles/github.css';

export default {
  data() {
    return {
      leakageInfo: {},
      code: '',
      form: { security: 1, ignore: 1, desc: '' }
    }
  }, methods: {
    fetchInfoData() {
      this.axios.get(`${this.GLOBAL.leakage}/${this.$route.params.id}/info`)
        .then((response) => {
          this.leakageInfo = response.data.result[0];
          this.form.security = this.leakageInfo.security;
          this.form.project = this.leakageInfo.project;
          this.form.ignore = this.leakageInfo.ignore;
          if (this.leakageInfo.desc) {
            this.form.desc = Base64.decode(this.leakageInfo.desc);
          }
        })
        .catch((error) => {
          this.$message.error(error.toString());
        });
    },
    fetchCodeData() {
      this.axios.get(`${this.GLOBAL.leakage}/${this.$route.params.id}/code`)
        .then((response) => {
          this.code = Base64.decode(response.data.result[0].code);

        })
        .catch((error) => {
          this.$message.error(error.toString());
        });
    },
    dealLeakage(form) {
      this.form.id = this.$route.params.id;
      this.axios.patch(this.GLOBAL.leakage, this.form
      )
        .then((response) => {
          this.$message.success(response.data.msg);
        })
        .catch((error) => {
          this.$message.error(error.toString());

        });
    }
  },
  mounted() {
    this.fetchInfoData();
    this.fetchCodeData();
    this.$nextTick(function () {

    });
  }
}
</script>

<style scoped>
@import "../style/github01.css";
@import "../style/github02.css";
</style>
