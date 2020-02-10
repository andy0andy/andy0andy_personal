from django.urls import path

from . import views

app_name = 'comments'

urlpatterns = [
    path('comment_post/<int:article_id>',views.comment_post,name="comment_post"),       # 评论
    path('tome/',views.comment_tome,name="tome"),       # 给我留言
]