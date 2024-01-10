# 在线考试系统
这个项目已经拖延了好几年了，2024年要重新开始动工，有需要这个项目做参考的同学，可以加我微信:MintBlueD，留言：GitHub  

到时候我会拉一个群，大家来说说，前端想用Vue、React还是Angular😏，截止在24年1月底哦～

---

功能模块有4大模块：`用户管理模块`、`试题管理模块`、`试卷管理模块`和`考试管理模块`

系统角色有3类：系统管理员、学生用户和教师用户

### 功能点  
#### 用户管理模块

+ [ ] 用户登录
  - [x] 登录接口  
  - [x] 登录JWT
 + [ ] 用户信息管理  
   - [ ] 学生信息管理
     - [ ] 学生信息新增接口
     - [ ] 学生信息编辑接口
     - [ ] 学生信息删除接口
     - [ ] 学生信息查询接口（List）
     - [ ] 学生信息查询接口（Detail）
   - [ ] 教师信息管理
     - [ ] 教师信息新增接口
     - [ ] 教师信息编辑接口
     - [ ] 教师信息删除接口
     - [ ] 教师信息查询接口（List）
     - [ ] 教师信息查询接口（Detail）
 + [ ] 用户激活   
 + [ ] 找回密码  
 + [ ] 用户消息  
 + [ ] 日志管理  

####  试题管理模块

 + [ ] 试题新增  
 + [ ] 试题修改  
 + [ ] 试题删除  
 + [ ] 试题筛选及排序  
 + [ ] 试题收藏  
 + [ ] 公共题库和私人题库的分类  
 + [ ] 错题查询及筛选（面向学生用户）  

####  试卷管理模块

 + [ ] 试卷新增  
 + [ ] 试卷修改  
 + [ ] 试卷删除  
 + [ ] 复制试卷  
 + [ ] 试卷查看  

####  考试管理模块

 + [ ] 新增考试  
 + [ ] 试卷答题（面向学生用户）  
 + [ ] 考试成绩查询  
 + [ ] 考试成绩下载  

#### 技术栈
服务端：Python 3.8 + Django 4.3.8

数据库：MySQL 8.2

#### MySQL安装
我是用Docker安装的MySQL，更加方便一些，下面👇是下载&启动命令：  
##### 下载

```
docker pull mysql:8.2
```

##### 启动容器  

```
docker run -p 3306:3307 --name mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:8.2
```


---
    PS：内容暂定，待完善。。。
