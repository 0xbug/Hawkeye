<script>
  const apiUri = '/api';
  const statistics = `${apiUri}/statistics`;
  const leakage = `${apiUri}/leakage`;
  const settingBlacklist = `${apiUri}/setting/blacklist`;
  const settingQuery = `${apiUri}/setting/query`;
  const settingCron = `${apiUri}/setting/cron`;
  const settingNotice = `${apiUri}/setting/notice`;

  export default{
    leakage,
    settingBlacklist,
    settingQuery,
    settingNotice,
    settingCron,
    statistics
  }
</script>
