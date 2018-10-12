import Vue from "vue";
const apiUri = "/api";
const trend = `${apiUri}/trend`;
const statistic = `${apiUri}/statistic`;
const leakage = `${apiUri}/leakage`;
const leakageInfo = `${apiUri}/leakage/info`;
const leakageCode = `${apiUri}/leakage/code`;
const settingBlacklist = `${apiUri}/setting/blacklist`;
const settingQuery = `${apiUri}/setting/query`;
const settingCron = `${apiUri}/setting/cron`;
const settingNotice = `${apiUri}/setting/notice`;
const settingMail = `${apiUri}/setting/mail`;
const settingDingTalk = `${apiUri}/setting/dingtalk`;
const settingGithub = `${apiUri}/setting/github`;
const api = {
  leakage,
  leakageCode,
  leakageInfo,
  settingBlacklist,
  settingQuery,
  settingNotice,
  settingCron,
  settingGithub,
  settingDingTalk,
  settingMail,
  statistic,
  trend
};
export default api;
Vue.prototype.api = api;
