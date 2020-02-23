from django.db import models

# Create your models here.
SEX = [
    ('男','男'),
    ('女','女')
]

DEPT = [
    ('学院一','学院一'),
    ('学院二','学院二'),
    ('学院三','学院三'),
    ('学院四','学院四')
]


# 学生表
class Student(models.Model):
    id = models.CharField(max_length=20,primary_key=True,verbose_name='学号')
    name = models.CharField(max_length=20,verbose_name='姓名')
    sex = models.CharField(max_length=4,choices=SEX,default='男',verbose_name='性别')
    dept = models.CharField(max_length=20,choices=DEPT,default=None,verbose_name='学院')
    major = models.CharField(max_length=20,default=None,verbose_name='专业')
    password = models.CharField(max_length=20,default='123',verbose_name='密码')
    email = models.EmailField(default=None,verbose_name='邮箱')
    birth = models.DateField(verbose_name='出生日期')

    class Meta:
        db_table = 'student'
        verbose_name= '学生'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id


# 教师表
class Teacher(models.Model):
    id = models.CharField(max_length=20,primary_key=True,verbose_name='教工号')
    name = models.CharField(max_length=20,verbose_name='姓名')
    sex = models.CharField(max_length=4,choices=SEX,default='男',verbose_name='性别')
    dept = models.CharField(max_length=20,choices=DEPT,default=None,verbose_name='学院')
    password = models.CharField(max_length=20,default='123456',verbose_name='密码')
    email = models.EmailField(default=None,verbose_name='邮箱')
    birth = models.DateField(verbose_name='出生日期')

    class Meta:
        db_table = 'teacher'
        verbose_name= '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 问题表
class Question(models.Model):
    ANSWER = [
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D')
    ]

    LEVEL = [
        ('1','easy'),
        ('2','general'),
        ('3','difficult')
    ]

    subject = models.CharField(max_length=20,verbose_name='科目')
    title = models.TextField(verbose_name='题目')
    optionA = models.CharField(max_length=30,verbose_name='选项A')
    optionB = models.CharField(max_length=30,verbose_name='选项B')
    optionC = models.CharField(max_length=30,verbose_name='选项C')
    optionD = models.CharField(max_length=30,verbose_name='选项D')
    answer = models.CharField(max_length=10,choices=ANSWER,verbose_name='答案')
    level = models.CharField(max_length=10,choices=LEVEL,default='1',verbose_name='难度')
    score = models.IntegerField(default=1,verbose_name='分数')

    class Meta:
        db_table = 'question'
        verbose_name = '单项选择题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<{} : {}>".format(self.subject,self.title)


# 试卷表
class Pager(models.Model):
    # 题号pid，和题库是多对多关系
    pid = models.ManyToManyField(Question)    
    # 教工号，和教师是一对多关系  
    tid = models.ForeignKey(Teacher,on_delete=models.CASCADE)

    subject = models.CharField(max_length=20,default="",verbose_name='科目')
    major = models.CharField(max_length=20,verbose_name='考卷适用专业')
    examtime = models.DateTimeField(verbose_name='考试时间')

    class Meta:
        db_table = 'pager'
        verbose_name='试卷'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.major



# 成绩表
class Grade(models.Model):
    # 学号sid，和学生是1对多关系
    sid = models.ForeignKey(Student,on_delete=models.CASCADE,default='')

    subject = models.CharField(max_length=20,default='',verbose_name='科目')
    grade = models.IntegerField(verbose_name='成绩')

    class Meta:
        db_table = 'grade'
        verbose_name = '成绩'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<{} : {}>".format(self.sid,self.subject)    