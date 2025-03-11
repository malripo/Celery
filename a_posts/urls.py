from django.urls import path, include
# from a_posts.views import home_view
from a_posts.views import *
from a_users.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('category/<tag>/', home_view, name='category'),
    path('create/', post_create_view, name='post-create'),
    path('delete/<pk>/', post_delete_view, name='post-delete'),
    path('edit/<pk>/', post_edit_view, name='post-edit'),
    path('<pk>/', post_page_view, name='post'),
    path('like/<pk>/', like_post, name="like-post"), 
    path('comment/like/<pk>/', like_comment, name="like-comment"), 
    path('reply/like/<pk>/', like_reply, name="like-reply"),
    path('commentsent/<pk>/', comment_sent, name="comment-sent"),
    path('comment/delete/<pk>/', comment_delete_view, name='comment-delete'),  
    path('replysent/<pk>/', reply_sent, name='reply-sent'), 
    path('replyform/<pk>/', reply_form, name='reply-form'),
    path('reply/delete/<pk>/', reply_delete_view, name='reply-delete'),  
]