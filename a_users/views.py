# from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from django.contrib import messages
# from django.contrib.sites.models import Site
from django.http import Http404
from django.contrib.auth.models import User
from allauth.account.utils import send_email_confirmation
from a_posts.forms import ReplyCreateForm
# from a_inbox.forms import InboxNewMessageForm
from .forms import *

# Create your views here.

# def profile_view(request):
def profile_view(request, username=None):

    # profile = request.user.profile
    
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
        
    posts = profile.user.posts.all()
    
    if request.htmx:
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            # return render(request, 'snippets/loop_profile_posts.html', { 'posts': posts })
        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            replyform = ReplyCreateForm()
            return render(request, 'snippets/loop_profile_comments.html', { 'comments': comments, 'replyform': replyform })
        elif 'liked-posts' in request.GET:
            posts = profile.user.likedposts.order_by('-likedpost__created') 
        return render(request, 'snippets/loop_profile_posts.html', { 'posts': posts })
    
    # new_message_form = InboxNewMessageForm()
    
    context = {
        'profile' : profile,
        'posts': posts,
        # 'new_message_form' : new_message_form
    }

    # return render(request, 'a_users/profile.html')    
    return render(request, 'a_users/profile.html', context)


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
            
#             if request.user.emailaddress_set.get(primary=True).verified:
#                 return redirect('profile')
#             else:
#                 return redirect('profile-verify-email') 
        
    if request.path == reverse('profile-onboarding'):
        template = 'a_users/profile_onboarding.html'
    else:
        template = 'a_users/profile_edit.html'

    # return render(request, 'a_users/profile_edit.html')
    # return render(request, 'a_users/profile_edit.html', {'form':form})          
    return render(request, template, {'form':form})


@login_required
def profile_delete_view(request):
    user = request.user
    
    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')
    
    return render(request, 'a_users/profile_delete.html' )


# def profile_verify_email(request):
#     send_email_confirmation(request, request.user)
#     return redirect('profile')

@login_required
def profile_settings_view(request):
    return render(request, 'a_users/profile_settings.html')

@login_required
def profile_emailchange(request):
    
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form':form})
    
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():
            
            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('profile-settings')
            
            form.save() 
            
            # Then Signal updates emailaddress and set verified to False
            
            # Then send confirmation email 
            send_email_confirmation(request, request.user)
            
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Form not valid')
            return redirect('profile-settings')
        
    return redirect('home')


@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect('profile-settings')

@login_required
def newsletter_subscribe(request):
    user = request.user
    user.profile.newsletter_subscribed = not user.profile.newsletter_subscribed
    user.profile.save()
    return redirect('profile-settings')