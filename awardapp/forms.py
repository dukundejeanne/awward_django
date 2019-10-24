from .models import Project,Comment,Profile,User
from django import forms
from django.forms import ModelForm,Textarea,IntegerField

class NewProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        exclude=['user','likes',]
        # widgets = {
        #     'tags': forms.CheckboxSelectMultiple(),
        # }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        exclude=['comment_image','posted_by','profile']

class UpdatebioForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['user','followers','following']

class NewsLetterForm(forms.Form):
    your_name=forms.CharField(label='First Name', max_length=40)
    email=forms.EmailField(label='Email')

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model=Profile
#         fields=['bio','profile_pic']

# class UserUpdateForm(forms.ModelForm):
#     email=forms.EmailField()
#     class Meta:
#         model=User
#         fields=['username','email']
