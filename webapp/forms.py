from django import forms 
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class AccountForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2',
        )

    def save(self, commit=True):
        user= super(AccountForm,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )

class AddForm(forms.ModelForm): 
  
    class Meta: 
        model = Posts
        fields = ['title', 'pic','body', 'post_date'] 
        