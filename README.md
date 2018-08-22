# OASysterm
# 简介：  
一个简单的公司OA平台系统，利用Django+Bootstrap框架搭建，实现流程发起、审批、查阅及用户管理等功能。 已部署至heroku，可访问地址:https://my-oasysterm-app-cn.herokuapp.com/ ,登录账号wangjie，密码1111.同样用Django复写的见Github https://github.com/venthent/OASysterm_By_Django


## 一、基本功能：  

1、登录、登出,并控制回话超时时间为10分钟，超过10分钟未进行任何操作则自动清除回话，再次刷新网页返回登录页面；  

2、由于是公司内部系统，故所有页面都设置视图保护，即所有页面都需要登录才能进入；  
3、权限管理，分为管理员（Administrator）权限以及普通用户（User）权限，管理员可以对所有用户增删改查，普通用户可修改用户的基本属性；所有的登录用户均为管理员添加；    
4、职位（Position）等级，从高到低依次设为老板（Boss）、经理（Manager）、普通职员（Staff）三个职级，流程流向为从低到高；老板默认权限是管理员，其他为普通用户；  
5、流程（Process）发起，创建一个流程，包括流程主题、内容、等级等，流程等级对应最终审批人的职级；老板不需要发起流程；  
6、流程审批，流程审批人在主页看到待审批的流程概要，并进行审批；可填入审批意见，选择同意与否，并发送至下一职级的审批人；  
7、流程查看，用户可查看自己发起的流程概况，包括流程状态（分为已通过、正在审批、未通过三种状态）、已审批人意见、下一位审批人等信息。   

## 二、流程关系图  
![image](https://github.com/venthent/OASysterm/raw/master/imgs/OA流程图.jpg)

## 三、实际运行效果
假设人员组织如图所示，发起流程的方向是从普通职员（Staff）到老板（Boss）：  
![image](https://github.com/venthent/OASysterm/raw/master/imgs/人员组织图.jpg)


1、登录页面：  

![image](https://github.com/venthent/OASysterm/raw/master/imgs/login-page.jpg)    
<br />
<br />

    
2、进入系统的主页面，也是待审批流程的概览页面：  
![image](https://github.com/venthent/OASysterm/raw/master/imgs/index-page.jpg)  
<br />
<br />


3、发起流程，创建流程内容；'Send to'表示要发送给谁审批：   

![image](https://github.com/venthent/OASysterm/raw/master/imgs/start-process.jpg)  


4、查看自己已经发起的流程情况，有三种状态：已通过（Passed）、未通过（Din't Pass）和正在审批中（Inspecting）:  

![image](https://github.com/venthent/OASysterm/raw/master/imgs/process-list.jpg)  
<br />
<br />


5、查看已经发起流程的详情，可以查看流程内容，审批人的意见以及下一位审批人    

![image](https://github.com/venthent/OASysterm/raw/master/imgs/detail-of-myprocess.jpg) 

<br />
<br />

6、系统管理，管理员可以看到所有用户信息并进行相应的修改、删除、增加，普通用户只能看到自己的信息并修改  

![image](https://github.com/venthent/OASysterm/raw/master/imgs/account-manage-page.jpg)    
<br />
<br />
7、账户信息修改页面，有三种情况：
>
>>(1).管理员用户修改自己的账号，修改页面如下：  

>>![image](https://github.com/venthent/OASysterm/raw/master/imgs/edit-account-page.jpg)  

<br />

>>(2).管理员修改其他人的账号，不能修改密码：  

>>![image](https://github.com/venthent/OASysterm/raw/master/imgs/edit-account-page2.jpg)  
<br />

>>(3).普通用户修改自己的账号：  

>>![image](https://github.com/venthent/OASysterm/raw/master/imgs/edit-account-page3.jpg)

