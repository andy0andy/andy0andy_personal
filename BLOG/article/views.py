from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
import markdown
import os
from django.core.paginator import Paginator
from django.db.models import Q

from .models import ArticlePost
from .forms import ArticlePostForm
from comments.models import Comments
from comments.forms import CommentsForm

# Create your views here.

# 文章列表
def article_list(request):
    context = {}

    order = request.GET.get('order')
    search = request.GET.get('search')
    tag = request.GET.get('tag')

    # 不显示 id=1 的用户的文章
    articles = ArticlePost.objects.exclude(author=User.objects.get(id=1))

    # 搜索
    if search != None and search:
        articles = articles.filter(Q(title__icontains=search) | Q(body__icontains=search))
    else:
        search = ""

    # 标签
    if tag != None and tag:
        articles = articles.filter(tags__name__in=[tag])
    else:
        tag = ""

    # 最热文章
    if order == 'article_hot':
        articles = articles.order_by('-looks')

    # 分页
    paginator = Paginator(articles,5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context['articles'] = articles
    context['order'] = order
    context['search'] = search
    context['tag'] = tag

    return render(request, 'article/article_list.html',context=context)

# 创建文章
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = get_object_or_404(User,id=request.user.id)
            new_article.save()
            # 如果提交的表单使用了commit = False选项
            # 则必须调用save_m2m()才能正确的保存标签
            article_post_form.save_m2m()
            return redirect(reverse("article:article_list"))
        else:
            return HttpResponse('表单无效:',article_post_form.errors)
    elif request.method == 'GET':
        context = {}
        context['article_post_form'] = ArticlePostForm()
        return render(request,'article/article_create.html',context=context)
    else:
        return HttpResponse("只允许POST/GET请求！！！")

def article_detail(request,id):
    context = {}

    article = get_object_or_404(ArticlePost,id=id)
    comments = Comments.objects.filter(article=id)

    article.looks += 1
    article.save(update_fields=['looks'])

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',        # 包含 缩写、表格等常用扩展
        'markdown.extensions.codehilite',       # 语法高亮扩展
        'markdown.extensions.toc',      # 文章栏目
    ])
    article.body = md.convert(article.body)

    context['article'] = article
    context['toc'] = md.toc
    context['comments'] = comments
    context['comments_form'] = CommentsForm()       # 前台应用富文本时使用

    return render(request,'article/article_detail.html',context=context)


def article_delete(request,id):
    # 加入bootstrap模态框，增加删除安全性
    if request.method == 'POST':
        article = get_object_or_404(ArticlePost,id=id)

        # 删除文章的同时也要删除相应的图片文件，减小空间
        # os.path.abspath(path): 获取绝对路径
        # os.path.join(path1,path2): 连接路径
        imgpath = article.title_img.name
        os.remove(os.path.abspath(os.path.join('D:\code\BLOG\media',imgpath)))

        # 如果删除的是最后一张图片，那么连文件夹也删除
        if not os.listdir(os.path.abspath(os.path.join('D:\code\BLOG\media',imgpath[:26]))):
            os.rmdir(os.path.abspath(os.path.join('D:\code\BLOG\media',imgpath[:26])))

        article.delete()
        return redirect(reverse('article:article_list'))
    elif request.method == 'GET':
        return redirect(reverse('article:article_detail',kwargs={'id':id}))
    else:
        return HttpResponse('只允许POST/GET请求！！！')


def article_update(request,id):
    context = {}
    article = get_object_or_404(ArticlePost, id=id)

    if request.method == 'POST':
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        if article_post_form.is_valid():
            article.title = request.POST.get('title')
            article.body = request.POST.get('body')
            if request.FILES.get('title_img'):
                # 更新时，先把旧图片删除
                imgpath = article.title_img.name
                os.remove(os.path.abspath(os.path.join('D:\code\BLOG\media',imgpath)))

                # 如果删除的是最后一张图片，那么连文件夹也删除
                if not os.listdir(os.path.abspath(os.path.join('D:\code\BLOG\media', imgpath[:26]))):
                    os.rmdir(os.path.abspath(os.path.join('D:\code\BLOG\media', imgpath[:26])))

                article.title_img = request.FILES.get('title_img')

            tag = request.POST.get('tags')
            # 记得加 * 号
            article.tags.set(*tag.split(','),clear=True)

            article.save()
            return redirect(reverse('article:article_detail',kwargs={'id':id}))
    elif request.method == 'GET':
        context['article'] = article
        context['article_post_form'] = ArticlePostForm()
        return render(request,'article/article_update.html',context=context)
    else:
        return HttpResponse('只允许POST/GET请求！！！')


def article_likes(request,id):
    article = get_object_or_404(ArticlePost,id=id)
    article.likes += 1
    article.looks -= 1
    article.save(update_fields=['likes','looks'])
    return redirect(reverse('article:article_detail',kwargs={'id':article.id}))