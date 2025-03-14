from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from .models import *
from .forms import *
# from django.forms import ModelForm
# from django import forms
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from django.core.paginator import Paginator
# from a_features.views import feature_enabled

# Create your views here.
def home_view(request, tag=None):
    # print('Hello')
    # print(request)
    # # print(request.META)
    # print ('request Method:', request.method)
    # if request.method == 'POST':
    #     print('Bye Bye')
    # title = 'Welcome to Django'    
    # return render(request, 'index.html', { 'title' : title })
    # return render(request, 'base.html', { 'title' : title })
    # return render(request, 'a_posts/home.html', { 'title' : title })
    # return render(request, 'a_posts/home.html')  
    
    # posts = Post.objects.all()
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()
    
    paginator = Paginator(posts, 3)
    page = int(request.GET.get('page', 1))   
    try:
        posts = paginator.page(page)
    except:
        return HttpResponse('')
    
    
    
    # categories = Tag.objects.all()  
    
    context = {
        'posts': posts,
        # 'categories': categories,  
        'tag': tag,   
        'page' : page,
        # 'feature_herobutton' : feature_herobutton     
    }

    if request.htmx:
        return render(request, 'snippets/loop_home_posts.html', context)
     
            
    # return render(request, 'a_posts/home.html', {'posts' : posts })
    return render(request, 'a_posts/home.html', context)    

# def category_view(request, tag):
#     posts =Post.objects.filter(tags__slug=tag)
#     return render(request, 'a_posts/home.html', {'posts' : posts })
    

# class PostCreateForm(ModelForm):
#     class Meta:
#         model =Post
#         # fields = '__all__'
#         fields = ['url', 'body']
#         labels = {
#             'body' : 'Caption'
#         }
#         widgets = {
#             'body' : forms.Textarea(attrs={'rows':3, 'placeholder':'Add a caption ...', 'class':'font1 text-4xl'}),
#             'url' : forms.TextInput(attrs={'placeholder':'Add a url ...'}),
#         }

@login_required    
def post_create_view(request):
    form = PostCreateForm()
    if request.method =='POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  
                
            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text, 'html.parser')
            find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            
            image = find_image[0]['content']
            # try:   
            #     image = find_image[0]['content']
            # except:
            #     messages.error(request, 'Requested image is not on Flickr!')
            #     return redirect('post-create')
            
            post.image = image
            
            find_title = sourcecode.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title
            
            find_artist = sourcecode.select('a.owner-name')
            artist = find_artist[0].text.strip() 
            post.artist = artist
            
            post.author = request.user
            
            post.save()
            form.save_m2m()
            return redirect('home')
     
    return render(request, 'a_posts/post_create.html', {'form' : form }) 

@login_required
# def post_delete_view(request):
def post_delete_view(request, pk):
    # post = Post.objects.get(id=pk)
    # post = get_object_or_404(Post, id=pk)
    post = get_object_or_404(Post, id=pk, author=request.user)
    
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post deleted')
        return redirect('home')

    # return render(request, 'a_posts/post_delete.html')        
    return render(request, 'a_posts/post_delete.html', {'post' : post})


@login_required
def post_edit_view(request, pk):
    # post = Post.objects.get(id=pk)
    # post = get_object_or_404(Post, id=pk)    
    post = get_object_or_404(Post, id=pk, author=request.user)
    form = PostEditForm(instance=post)
    
    if request.method == "POST":
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid:
            form.save()
            messages.success(request, 'Post updated')
            return redirect('home')
    
    context = {
        'post' : post,
        'form' : form
    }

    return render(request, 'a_posts/post_edit.html', context)


def post_page_view(request, pk):
    # post = Post.objects.get(id=pk)
    post = get_object_or_404(Post, id=pk)
    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()
    
    # categories = Tag.objects.all()

    # if request.META.get("HTTP_HX_REQUEST"):
    # if request.htmx:
    #     comments = post.comments.all()
    #     return render(request, 'snippets/loop_postpage_comments.html', {'comments': comments})        
            
    if request.htmx:
        if 'top' in request.GET:
            # comments = post.comments.filter(likes__isnull=False)
            # comments = post.comments.filter(likes__isnull=False).distinct()
            # comments = post.comments.annotate(num_likes=Count('likes')).order_by('-num_likes')            
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
            
        return render(request, 'snippets/loop_postpage_comments.html', {'comments': comments, 'replyform': replyform})
    
    context = {
        'post' : post,
        'commentform' : commentform,
        'replyform' : replyform,
        # 'categories' : categories,
    }
    
    return render(request, 'a_posts/post_page.html', context)


@login_required 
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    replyform = ReplyCreateForm()
    
    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post            
            comment.save()
            
    context = {
        'post' : post,
        'comment': comment,
        'replyform': replyform
    }

    # return redirect('post', post.id)
    # return render(request, 'a_posts/comment.html', context)
    return render(request, 'snippets/add_comment.html', context)


@login_required 
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    replyform = ReplyCreateForm()
    
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid:
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment            
            reply.save()
            
    context = {
        'reply' : reply,
        'comment': comment,
        'replyform': replyform
    }

    # return redirect('post', comment.parent_post.id)
    return render(request, 'snippets/add_reply.html', context)

@login_required 
def reply_form(request, pk):
    reply = get_object_or_404(Reply, id=pk)
    replyform = NestedReplyCreateForm()
    
    if request.method == 'POST':
        form = NestedReplyCreateForm(request.POST)
        if form.is_valid:
            reply_nested = form.save(commit=False)
            reply_nested.author = request.user
            reply_nested.parent_reply = reply 
            reply_nested.level = reply.level + 1 
            reply_nested.save()
            return render(request, 'a_posts/reply.html', {'reply': reply_nested})
      
    context = {
        'reply' : reply,
        'replyform': replyform
    }
    return render(request, 'snippets/add_replyform.html', context)

@login_required
def comment_delete_view(request, pk):
    post = get_object_or_404(Comment, id=pk, author=request.user)
    
    if request.method == "POST":
        post.delete()
        messages.success(request, 'Comment deleted')
        return redirect('post', post.parent_post.id )
        
    return render(request, 'a_posts/comment_delete.html', {'comment' : post})


# @login_required
# def reply_delete_view(request, pk):
#     reply = get_object_or_404(Reply, id=pk, author=request.user)
    
#     if request.method == "POST":
#         reply.delete()
#         messages.success(request, 'Reply deleted')
#         return redirect('post', reply.parent_comment.parent_post.id )
        
#     return render(request, 'a_posts/reply_delete.html', {'reply' : reply})

@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)
    reply.delete()
    return HttpResponse('')   

'''
def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            ...
            return func(request, *args, **kwargs)
        return wrapper
    return inner_func    
'''
'''
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    user_exist = post.likes.filter(username=request.user.username).exists()

    if post.author != request.user:
        if user_exist:
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

    # return redirect('post', post.id)
    # return HttpResponse( post.likes.count())    
    return render(request, 'snippets/likes.html', {'post' : post })
'''

def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            post = get_object_or_404(model, id=kwargs.get('pk'))
            user_exist = post.likes.filter(username=request.user.username).exists()
            
            if post.author != request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)
                    
            return func(request, post)
        return wrapper
    return inner_func


@login_required
@like_toggle(Post)
def like_post(request, post):   
    return render(request, 'snippets/likes.html', {'post' : post })


@login_required
@like_toggle(Comment)
def like_comment(request, post):   
    return render(request, 'snippets/likes_comment.html', {'comment' : post })


@login_required
@like_toggle(Reply)
def like_reply(request, post):   
    return render(request, 'snippets/likes_reply.html', {'reply' : post })           