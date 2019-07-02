module.exports = {
  runtimeCompiler: true,

  css: undefined,

  chainWebpack: config => {
    config.module
      .rule("vue")
      .use("vue-loader")
      .loader("vue-loader")
      .tap(options => {
        return options;
      });
  },
  devServer: {
    proxy: {
      "/api/": {
        target: "http://0.0.0.0:8999",
        changeOrigin: true
      }
    }
  },
  baseUrl: undefined,
  outputDir: undefined,
  assetsDir: undefined,
  filenameHashing: true,
  productionSourceMap: false,
  parallel: undefined
};
