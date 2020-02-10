from django.shortcuts import render,reverse,redirect,get_object_or_404
from django.http import HttpResponse

from .models import Comments
from .forms import CommentsForm
from article.models import ArticlePost

# Create your views here.

def comment_post(request,article_id):
    if request.method == 'POST':
        article = get_object_or_404(ArticlePost,id=article_id)
        comments_form = CommentsForm(request.POST)
        if comments_form.is_valid():
            new_comments = comments_form.save(commit=False)
            new_comments.article = article
            new_comments.user = request.user
            new_comments.save()
            return redirect(reverse('article:article_detail',kwargs={'id':article_id}))
    else:
        return HttpResponse('只允许POST请求！！！')

def comment_tome(request):
    article = get_object_or_404(ArticlePost,id=1)

    if request.method == 'POST':
        comments_form = CommentsForm(request.POST)
        if comments_form.is_valid():
            new_comment = comments_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(reverse("comments:tome"))
    elif request.method == 'GET':
        context = {}

        comment_tome = Comments.objects.filter(article=article)

        context['comment_tome'] = comment_tome
        context['comment_form'] = CommentsForm()

        return render(request,'comments/tome.html',context=context)
    else:
        return HttpResponse("只允许POST/GET请求！！！")