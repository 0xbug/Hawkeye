# Hawkeye

[![GitHub issues](https://img.shields.io/github/issues/0xbug/Hawkeye.svg)](https://github.com/0xbug/Hawkeye/issues)
[![GitHub forks](https://img.shields.io/github/forks/0xbug/Hawkeye.svg)](https://github.com/0xbug/Hawkeye/network)
[![GitHub stars](https://img.shields.io/github/stars/0xbug/Hawkeye.svg)](https://github.com/0xbug/Hawkeye/stargazers)
[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) 
[![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/0xbug/Hawkeye/master/LICENSE)

## 简介

> 监控github代码库，及时发现员工托管公司代码到GitHub行为并预警，降低代码泄露风险。

## 截图

![Hawkeye](https://user-images.githubusercontent.com/12611275/38987328-db9736d6-4401-11e8-9299-b5d1bb9c6b2e.png)

## **最近更新**

- 2018-04-19 v2.0.0
    - 添加Basic 认证, 必须按照新的 `config.ini.example` 重新进行相关配置 
    - 用户体验优化,支持多种过滤方式
    - 爬虫任务状态、结果记录展示
    - 解析受影响资产
    - 添加开关，控制是否抓取
    - 邮件 告警聚合
- 2018.03.14 
    - 由于 spider.py 中一处正则匹配问题，导致近日开始登录失败，请大家 pull 下新代码


## 特性

- 周期监测
- web管理
- 邮箱告警通知
- 黑名单添加
- 爬虫任务设置

## 依赖

*   Python 3.x
*   Flask
*   MongoDB

## 支持平台

*   Linux, macOS


## 安装

克隆项目到本地

```bash
git clone https://github.com/0xbug/Hawkeye.git --depth 1
```


Hawkeye 支持 Python *3.x* on Linux and macOS。(2.x兼容性 需自行修改测试)

安装依赖 (修改/usr/local/bin/python3 为你系统的Python 3 路径)

```bash
cd Hawkeye
pip install virtualenv
virtualenv --python=/usr/local/bin/python3 venv
source venv/bin/activate
pip install -r deploy/requirements.txt

```


## 设置

```bash
cp config.ini.example config.ini
vim config.ini
```

### 需要修改的配置

- 平台认证配置(BasicAuth)
```conf
[Auth]
ENABLE = 1 或者 0 #是否开启认证功能
TYPE = basic #(暂时只支持basic认证)
USERNAME = 帐号
PASSWORD = 密码
```


- `github` 帐户配置
```conf
[GitHub]
USERNAME = 帐号
PASSWORD = 密码
```
- `MongoDB` 认证配置(可选)

先创建用户
```bash
mongo
>db.createUser({user:'root',pwd:'password',roles:[{role:'dbOwner',db:'Hawkeye'}]})
```
然后修改配置文件
```conf
[MongoDB]
HOST = localhost
PORT = 27017
ACCOUNT = 帐号
PASSWORD = 密码
```

- 告警配置（`ENABLE`:是否开启告警功能）

```conf
[Notice]
ENABLE = 1
MAIL_SERVER = 邮件服务器
MAIL_PORT = smtp端口
FROM = 发件人
PASSWORD = 密码
```

## 运行

```bash
python Hawkeye.py
```
然后访问 http://0.0.0.0:5000/ 进行关键词、告警、黑名单、定时任务配置(初次运行需要点击确认按钮新建cron任务)。

## 部署

建议使用 `supervisor` 设置成开机自启，并监控进程，配置文件 `deploy/Hawkeye.conf.example`

## 说明

> 如果对您有帮助，您可以点右上角 Star 支持一下 谢谢！
或者您可以 [follow](https://github.com/0xbug?utf8=%E2%9C%93&tab=repositories&q=&type=source&language=) 一下