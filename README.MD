# Hawkeye

[![GitHub issues](https://img.shields.io/github/issues/0xbug/Hawkeye.svg)](https://github.com/0xbug/Hawkeye/issues)
[![GitHub forks](https://img.shields.io/github/forks/0xbug/Hawkeye.svg)](https://github.com/0xbug/Hawkeye/network)
[![GitHub stars](https://img.shields.io/github/stars/0xbug/Hawkeye.svg)](https://github.com/0xbug/Hawkeye/stargazers)
[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) 
[![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/0xbug/Hawkeye/master/LICENSE)

## 简介

> 监控github代码库，及时发现员工托管公司代码到GitHub行为并预警，降低代码泄露风险。

## 截图

![Hawkeye](https://user-images.githubusercontent.com/12611275/46849889-0d2d0980-ce24-11e8-832e-35f6f935bf3b.png)
## **最近更新**
- 2018-10-12 v3.0.0 非兼容性更新,需配置新数据库
    - 搜索方式切换成API，支持添加多GitHub用户，API配额可视化
    - 配置可视化，去除配置文件
    - crontab 切换成轻量级的任务队列 Huey ,任务周期可自定义
    - 支持 Docker 部署
    - 支持批量忽略
    - 爬虫任务状态、结果记录展示
    - 优化解析受影响资产
    - 重构邮件 告警，添加钉钉告警


## 特性

- 周期监测
- web管理
- 邮箱告警通知
- 黑名单添加
- 爬虫任务设置

## 依赖

*   Python 3.x
*   Flask
*   MongoDB >= 3.x

## 支持平台

*   Linux, macOS


## 安装(Docker 部署)
```
docker pull daocloud.io/0xbug/hawkeye
```
或者手动 build

克隆项目到本地

```bash
git clone https://github.com/0xbug/Hawkeye.git --depth 1
cd Hawkeye
docker build -t hawkeye .
docker run -ti -p 80:80 -e MONGODB_URI=mongodb://username:password@ip:27017/hawkeye -e MONGODB_USER= -e MONGODB_PASSWORD= -d hawkeye ## mongodb 需认证
docker run -ti -p 80:80 -e MONGODB_URI=mongodb://ip:27017 -d hawkeye ## mongodb 无认证

```


Hawkeye 支持 Python *3.x* on Linux and macOS。(2.x兼容性 需自行修改测试)



## 捐赠

> 如果该项目对您有帮助，您可以捐赠支持一下 谢谢！

![](https://user-images.githubusercontent.com/12611275/48882508-a9035980-ee55-11e8-9b2f-59346504e196.png)
