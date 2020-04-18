# hellofamily个人网站（后端）
![](https://img.shields.io/badge/version-2.0-%23E5457D) ![](https://img.shields.io/pypi/v/Django/3.0.3?label=Django) ![](https://img.shields.io/pypi/v/celery/4.4.1?label=celery)![](https://img.shields.io/pypi/v/djangorestframework?label=djangorestframework)![](https://img.shields.io/pypi/v/channels?label=channels) ![](https://img.shields.io/pypi/v/aiohttp/3.6.2?label=aiohttp) 

[http://hellofamily.club](http://hellofamily.club)

有着各种各样奇怪的功能。神奇的图片库，H!P的新闻动态存档，小小的文章分享，以及后续会增加的好玩的东西。

## 模块划分

## 用户系统

### 登录/注册

- http://hellofamily.club/login 登录与注册页面

### 权限管理

- 默认权限为普通，可以浏览页面
- 管理员权限可进入管理页面，对平台的数据进行管理

## 管理功能

### 管理页面

![](http://cdn.hellofamily.club/Jietu20200418-1706052x.jpg)

### 功能模块

#### 图片库管理

- 图片库Cookie更新，人脸注册更新
- 组合管理
- 成员管理

#### 文章管理

- 文章分类管理
- 文章标签管理
- 文章管理（仅删除）

#### 用户管理

- 用户信息修改

#### 常规管理

- 登录页面走马灯图片管理

#### 动态管理

- HP官网动态分类管理
- 动态文章管理



## 图片库

### 图片收集

- 定时任务管理从微博爬虫下载图片的脚本，cookie失效时邮件通知更新cookie。
- 图片存入mongo数据库。
- 定时执行百度人脸识别API，识别人脸信息，并更新进mongo数据库中信息。

### 图片搜索

- 可按照组合，成员进行搜索图片，可选择两位成员，指定搜索只包含这两位成员的图片
- 页面可选`卡片模式`和`时间线模式`展示图片
- 页面上可手动更新图片的人脸识别结果，调用接口后，通过celery任务执行识别任务，识别成功后webscoket推送识别结果。

## 动态

### 动态收集

- 利用aiohttp异步库定时从HP官网爬虫下载演唱会、新闻、活动等信息，最后数据清洗入库采用celery任务。

### 动态搜索

- 可按照组合，成员，分类搜索

## 文章

### 文章编写

- 使用braft-editor富文本编辑器，编辑文章时，定时存储草稿，避免文章丢失。

### 文章检索

- 可按分类、标签、作者、标题检索

### 文章评论

- 可以发表评论，发表后评论会通过websocket推送给文章作者