"""a_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from a_posts.views import home_view
# from a_posts.views import *
from a_home.views import *
# from a_users.views import *

# for media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # for theboss
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # path('admin/', admin.site.urls),
    path('theboss/', admin.site.urls),
    
    # for allauth
    path('accounts/', include('allauth.urls')),
    path('profile/', include('a_users.urls')),
    path('post/', include('a_posts.urls')),
    path('', home_view, name='mainhome'),
    path('chat/', include('a_rtchat.urls')),
    path('ajax/', include('ajaxmethods.urls')),
    path('messageboard/', include('a_messageboard.urls')),
]
# for media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
