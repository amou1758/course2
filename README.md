# course2
对course项目进行重构，优化

### 学生选课系统
#### 主要包含3个部分
	
#### 教务
+ 教务可以发布课程，主要包括课程名，课程号，学分等信息
+ 教务可以发布通知，可以分类进行通知
+ 教务可以有审批权限，教师申请后课程，必须教务审批通过后，改课程才能进行后续操作
+ 教务可以对课程，通知，学生，教师进行编辑，删除
+ 对教师和学生进行密码重置

#### 教师
+ 教师申请课程，需要指定上课时间和上课地点，还有课程授课人数
+ 教务审批课程后，教师可以对课程进行上线，学生们就可以进行选课，默认上线时间为3天，会自动关闭
+ 在课程上线后，教师可以根据情况，适当延迟选课时间和课程容纳人数
+ 自动生成教学表
+ 可以下载每门课程的选课学生信息excel

#### 学生
+ 选课
+ 生成课程表

#### 个人中心
+ 头像设置
+ 个人资料设置

### 流程很简单，如图：
![image](https://github.com/wolflikai/course2/blob/master/dia.png)
