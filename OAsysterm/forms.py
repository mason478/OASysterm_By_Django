from django import forms
from django.forms import ValidationError,ModelForm
from django.contrib.auth.hashers import make_password,check_password
from .models import ProcessComments,MyUser,Position,Processes


#  构造审批流程的表单
class ApprovalFrom(forms.Form):
    CHOICES=[('agree', 'Agree'), ('disagree', 'Disagree')]
    comments=forms.CharField(label='Comments:',widget=forms.Textarea(
        attrs={'class':'form-control','placeholder':"Please input your comments"}))
    agreement=forms.ChoiceField(label='Agree?',choices=CHOICES)

    def save(self,author,process):
        cd=self.cleaned_data
        comments=cd['comments']
        agreement=cd['agreement']
        ProcessComments.objects.create(comments=comments,comments_stauts=agreement,
                                       comments_author=author,process=process)

# 构造添加新账户表单
class AddAccountForm(forms.Form):
    #  职位有3个,Staff,Manager,Boss
    CHOICES = [('Staff', 'Staff'), ('Manager', 'Manager'), ('Boss', 'Boss')]
    username=forms.CharField(label='Username:',widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Username for login'}))

    realname=forms.CharField(label='Real Name:',widget=forms.TextInput(
        attrs={'class':'form-control'}))
    position=forms.ChoiceField(label='Job position:',choices=CHOICES,widget=forms.Select(attrs={'class':'form-control'}))


    old_password=forms.CharField(label='Old password:',required=False,widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder': 'If you write nothing,origional password will not be changed.'}),)

    new_password=forms.CharField(label='New password:',required=False,widget=forms.PasswordInput(
        attrs={'class':'form-control',}))

    confirm_password=forms.CharField(label="Confirm new password:",required=False,widget=forms.PasswordInput(
        attrs={'class':'form-control',}))
    is_admin = forms.BooleanField(label='Is Administrator?', required=False)

    #def clean_username(self):
     #   username=self.cleaned_data['username']
      #  if MyUser.objects.filter(username=username).exists():
       #     raise ValidationError("The Account name already exists,please try another one.")
        #return username


    def save(self):
        cd=self.cleaned_data
        username=cd['username']
        realname=cd['realname']
        position=cd['position']
        p=Position.objects.filter(position_name=position).first()
        is_admin=cd['is_admin']
        #  在添加用户的时候，不需要手动设置密码,默认密码是'1111',密码采用哈希值保存
        MyUser.objects.create(username=username,password=make_password('1111'),
                              real_name=realname,position=p,is_admin=is_admin)

    def check_username(self):
        '''检查输入框的用户名，防止重复'''
        username = self.cleaned_data['username']
        if MyUser.objects.filter(username=username).exists():
            return False
        return True
    def check_new_and_old_password(self):
        '''检查输入框的密码情况'''
        if self.cleaned_data['old_password'] != '' and self.cleaned_data['new_password'] != '' and \
                self.cleaned_data['new_password'] == self.cleaned_data['confirm_password']:
            return True
        return False








