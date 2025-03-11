from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User

# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         # fields = '__all__'
#         exclude = ['user']
#         labels = {
#             'realname' : 'Name'
#         }
#         widgets = {
#             'image': forms.FileInput(),
#             'bio' : forms.Textarea(attrs={'rows':3})
#         }

# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image', 'displayname', 'info' ]
#         widgets = {
#             'image': forms.FileInput(),
#             'displayname' : forms.TextInput(attrs={'placeholder': 'Add display name'}),
#             'info' : forms.Textarea(attrs={'rows':3, 'placeholder': 'Add information'})
#         }

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        # fields = '__all__'
        exclude = ['user','email','location','newsletter_subscribed']

        # labels = {
        #     'realname' : 'Name',
        #     'bio' : 'Info'
        # }

        labels = {
            'image' :'',
            'realname' : '',
            'bio' : ''
        }    
            
        widgets = {
            'image': forms.FileInput(),
            'realname' : forms.TextInput(attrs={'placeholder': 'Add display name'}),
            'bio' : forms.Textarea(attrs={'rows':3,'placeholder': 'Add information'})
        }

class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email'] 