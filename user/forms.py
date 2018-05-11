from django import forms
from django.forms import extras
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from datetime import datetime
from string import ascii_letters as letters
from string import digits, punctuation


VALID_USERNAME_CHARS = letters + "._" + digits
VALID_PASSWORD_CHARS = letters + punctuation + digits

from user.models import Documents


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Documents
        fields = {'id', 'title', 'abstract', 'publisher', 'document', 'branch', 'visibilty', 'user_id', 'folder_label'}
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Add Title', }),
            'publisher': forms.TextInput(attrs={'placeholder': 'Add Publisher'}),
            'abstract': forms.Textarea(attrs={'rows': 4},),

        }

    # def clean(self):
    #     super(DocumentForm, self).clean()
    #     import os
    #     value = self.cleaned_data["document"]
    #     ext = os.path.splitext(value.name)[1]
    #     valid_extensions = ['.pdf', '.doc', '.docx']
    #     if not ext in valid_extensions:
    #         raise forms.ValidationError(u'File not supported!')
    #     return value


class UserRegistrationForm(forms.Form):
    name = forms.CharField(max_length=30, help_text='Full Name')
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    dob = forms.DateField(widget=extras.SelectDateWidget(
        years=range(1990, datetime.now().year + 1)), help_text='Date of Birth'
    )
    CSE = 'CSE'
    ECE = 'ECE'
    EEE = 'EEE'
    ME = 'ME'
    CE = 'CE'
    branchs = (
        (CSE, 'Computer Science and Engineering'),
        (ECE, 'Electronic and Communincation'),
        (EEE, 'Electrical and Electronic Engineering'),
        (ME, 'Mechanical Engineering'),
        (CE, 'Civil Engineering'),
    )
    department = forms.ChoiceField(choices=branchs, initial=CSE)
    student = 'st'
    faculty = 'fac'
    positions = (
        (student, 'Student'),
        (faculty, 'Faculty'),
    )
    position = forms.ChoiceField(choices=positions, initial=student)

    def clean_username(self):
        u_name = self.cleaned_data['username']
        if u_name.strip(VALID_USERNAME_CHARS):
            msg = "Only letters, digits, period and underscore characters are allowed in username"
            raise forms.ValidationError(msg)
        try:
            User.objects.get(username__exact=u_name)
            raise forms.ValidationError("Username already exists")
        except User.DoesNotExist:
            return u_name

    def clean_password(self):
        pwd = self.cleaned_data['password']
        if pwd.strip(VALID_PASSWORD_CHARS):
            raise forms.ValidationError("Only letters, digits and punctuation are allowed in password")
        return pwd

    def save(self):
        u_name = self.cleaned_data['username']
        u_name = u_name.lower()
        pwd = self.cleaned_data['password']
        email = self.cleaned_data['email']
        new_user = User.objects.create_user(u_name, email, pwd)
        new_user.name = self.cleaned_data['name']
        new_user.dob = self.cleaned_data['dob']
        new_user.department = self.cleaned_data['department']
        new_user.position = self.cleaned_data['position']
        new_user.save()


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def clean(self):
        super(UserLoginForm, self).clean()
        try:
            u_name, pwd = self.cleaned_data["username"], self.cleaned_data["password"]
            user = authenticate(username=u_name, password=pwd)
        except Exception:
            raise forms.ValidationError("Username and/or Password is not entered")
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return user
