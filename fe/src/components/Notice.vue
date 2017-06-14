<template>

  <el-card class="item">
    <el-tooltip content="邮箱格式：username@domain.com" placement="bottom-end">
      <i class="el-icon-information"></i>
    </el-tooltip>

    <el-tag
      :key="mail"
      v-for="mail in noticeMails"
      :closable="true"
      :close-transition="true"
      @close="handleDeleteNotice(mail)"
    >
      {{mail.keyword}}
    </el-tag>
    <el-input
      class="input-new-tag"
      v-if="inputVisible"
      v-model="inputValue"
      ref="saveTagInput"
      size="mini"
      @keyup.enter.native="handleInputNoticeConfirm"
      @blur="handleInputNoticeConfirm"
    >
    </el-input>
    <el-button v-else size="small" @click="showInput">添加</el-button>
  </el-card>


</template>
<script>
  export default {
    data () {
      return {
        enable: false,
        inputVisible: false,
        inputValue: '',
        noticeMails: []
      }
    },
    methods: {
      showInput() {
        this.inputVisible = true;
        this.$nextTick(_ => {
          this.$refs.saveTagInput.$refs.input.focus();
        });
      }, handleInputNoticeConfirm() {
        if (this.inputValue) {
          this.noticeMails.push({'keyword': this.inputValue});
          this.axios.post(this.GLOBAL.settingNotice, {'keyword': this.inputValue})
            .then((response) => {
              this.$message.success(response.data.msg);
              this.noticeMails = response.data.result;
            })
            .catch((error) => {
              this.$message.error(error.toString());
            });
        }
        this.inputVisible = false;
        this.inputValue = '';

      },

      handleDeleteNotice(mail) {
        this.noticeMails.splice(this.noticeMails.indexOf(mail), 1);
        this.axios.delete(`${this.GLOBAL.settingNotice}?keyword=${mail.keyword}`)
          .then((response) => {
            this.$message.success(response.data.msg);
            this.inputVisible = false;
            this.noticeMails = response.data.result;
          })
          .catch((error) => {
            this.$message.error(error.toString());
            this.inputVisible = false;
          });
      },
      fetchNoticeMails(){
        this.axios.get(this.GLOBAL.settingNotice)
          .then((response) => {
            this.noticeMails = response.data.result;
          })
          .catch((error) => {
            this.$message.error(error.toString());
          });
      }

    },
    mounted: function () {
      this.fetchNoticeMails();
      this.$nextTick(function () {
      });
    }
  }
</script>
<style scoped>
  .input-new-tag {
    margin-left: 10px;
    margin-right: 10px;
    width: 78px;
    margin-top: 5px;
    vertical-align: bottom
  }

  .input-new-tag .el-input__inner {
    height: 24px
  }
</style>
