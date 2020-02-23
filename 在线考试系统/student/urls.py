from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('studentLogin/',views.studentLogin,name="studentLogin"),
    path('teacherLogin/',views.teacherLogin,name="teacherLogin"),
    path('logOut/',views.logOut,name="logOut"),
    path('startExam/',views.startExam,name="startExam"),
    path('calGrade/',views.calGrade,name="calGrade"),
]