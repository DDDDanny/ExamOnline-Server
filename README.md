<div>
  <p align="center"><img src="READMELogo.png" style="zoom:20%;width:20%;" /></p>
</div>

# 在线考试系统（后端）

这个项目已经拖延了好几年了，2024年要重新开始动工，有需要这个项目做参考的同学，可以加我微信:MintBlueD，留言：GitHub + 你的问题

👉：如果你有想做的需求，可以提issue，我会尽量安排～

👉：不会没关系，我可以给你方向，但我不会教你。没有脑子的就别加了！

前端项目：https://github.com/DDDDanny/ExamOnline-Front

---

**功能模块有4大模块：**

`用户管理模块`、`试题管理模块`、`试卷管理模块`和`考试管理模块`

**系统角色有3类：**

`系统管理员`、`学生用户`和`教师用户`

---

#### 技术栈

服务端：Python 3.8 + Django 4.3.8

数据库：MySQL 8.2

---

#### 安装依赖

```bash
pip install -r requirements.txt
```

#### MySQL安装

我是用Docker安装的MySQL，更加方便一些，下面👇是下载&启动命令：  
##### 下载

```bash
docker pull mysql:8.2
```

##### 启动容器  

```bash
docker run -p 3306:3307 --name mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:8.2
```

---

#### 数据迁移

数据库安装完成后，新建`exam_online`库，然后执行👇的命令

```bash
python3 manage.py makemigrations
```

```bash
python3 manage.py migrate
```

数据迁移完成后，检查数据表

#### 导入预制数据

迁移完成后，导入预制`菜单项`、`教师用户`

```bash
python3 manage.py loaddata initial_data.json
```

⚠️ 注意：导入预制数据前需要先进行migrate。由于预制数据会在开发过程中发生变化，如果更新预制数据，最好先清表，再重新导入。

---

#### 启动项目

预制数据创建完成后，就可以启动项目了

```bash
python manage.py runserver
```

也可以配置Pycharm或是VSCode启动项

---

```
PS：内容暂定，待完善。。。
```

