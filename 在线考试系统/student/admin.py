from django.contrib import admin

from .models import Student,Teacher,Question,Pager,Grade
# Register your models here.

admin.site.site_header='在线考试系统后台'
admin.site.site_title='在线考试系统'

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','name','sex','dept','major','password','email','birth']
    # 点击那些元素进入编辑页面
    list_display_links = ['id','name']
    list_filter = ['name','dept','major','birth']
    search_fields = ['name','dept','major','birth']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sex', 'dept', 'password', 'email', 'birth']
    list_display_links = ['id', 'name'] 
    list_filter = ['name','dept']
    search_fields = ['name', 'dept', 'birth'] 


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','subject','title','optionA','optionB','optionC','optionD','answer','level','score']

    list_filter = ['subject','level']
    search_fields = ['subject','title','level','score']


@admin.register(Pager)
class PagerAdmin(admin.ModelAdmin):
    list_display = ['tid','subject','major','examtime']

    list_filter = ['subject','major']
    search_fields = ['tid','subject','major']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['sid','subject','grade']

    list_filter = ['subject']
    search_fields = ['sid','subject']