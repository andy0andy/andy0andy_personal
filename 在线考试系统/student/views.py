from django.shortcuts import render,redirect,reverse
# 退出登陆
from django.contrib.auth import authenticate,login,logout

from .models import Student,Teacher,Question,Pager,Grade

# Create your views here.

def index(request):
    return render(request,"student/index.html")


# 学生登陆
def studentLogin(request):
    context = {}

    if request.method == 'POST':
        stuId = request.POST.get('id')
        stuPwd = request.POST.get('password')

        student = Student.objects.get(id=stuId)

        if student.password == stuPwd:
            pagers = Pager.objects.filter(major=student.major)
            grades = Grade.objects.filter(sid=student.id)

            context['person'] = student
            context['pagers'] = pagers
            context['grades'] = grades

            return render(request,"student/index.html",context=context)
        else:
            context['message'] = '密码错误 T.T'
            return render(request,'student/index.html',context=context)

# 教师登陆
def teacherLogin(request):
    context = {}

    if request.method == 'POST':
        teaId = request.POST.get('id')
        teaPwd = request.POST.get('password')

        teacher = Teacher.objects.get(id=teaId)
        if teacher.password == teaPwd:
            pagers = Pager.objects.filter(tid=teaId)

            context['person'] = teacher
            context['pagers'] = pagers

            return render(request,"student/index.html",context=context)
        else:
            context['message'] = '密码错误 T.T'
            return render(request,'student/index.html',context=context)


# 退出登陆
def logOut(request):
    logout(request)
    return redirect(reverse("index"))

# 开始考试
def startExam(request):
    context = {}

    sid = request.GET.get('sid')
    subject = request.GET.get('subject')

    context['student'] = Student.objects.get(id=sid)
    context['pagers'] = Pager.objects.filter(subject=subject)
    context['subject'] = subject

    return render(request,"student/exam.html",context=context)


# 记分
def calGrade(request):
    context = {}

    if request.method=='POST':
        # 得到学号和科目
        sid=request.POST.get('sid')
        subject = request.POST.get('subject')

        # 重新生成Student实例，Paper实例，Grade实例，名字和index中for的一致，可重复渲染
        student= Student.objects.get(id=sid)
        pagers = Pager.objects.filter(major=student.major)
        grades = Grade.objects.filter(sid=student.id)

        # 计算该门考试的学生成绩
        question= Pager.objects.filter(subject=subject).values("pid").values('pid__id','pid__answer','pid__score')

        mygrade=0#初始化一个成绩为0
        for p in question:
            qId=str(p['pid__id'])#int 转 string,通过pid找到题号
            myans=request.POST.get(qId)#通过 qid 得到学生关于该题的作答
            # print(myans)
            okans=p['pid__answer']#得到正确答案
            # print(okans)
            if myans==okans:#判断学生作答与正确答案是否一致
                mygrade+=p['pid__score']#若一致,得到该题的分数,累加mygrade变量

        #向Grade表中插入数据
        Grade.objects.create(sid_id=sid,subject=subject,grade=mygrade)
        
        context['person'] = student
        context['pagers'] = pagers
        context['grades'] = grades 

        # 重新渲染index.html模板
        return render(request,'student/index.html',context = context)
