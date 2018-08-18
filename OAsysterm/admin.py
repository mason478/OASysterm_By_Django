from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin
from .models import MyUser,Processes

'''
class UserCreationForm(forms.ModelForm):
    """A form for creating new users."""
    class Meta:
        model=MyUser
        fields=('username','real_name','position')

    def save(self, commit=True):
        user=super().save(commit=True)

        #  预设密码 '1111'
        user.set_password('1111')

        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password=ReadOnlyPasswordHashField()

    class Meta:
        model=MyUser()
        fields=('username','real_name','is_admin')

class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username','real_name','is_admin')
    list_filter = ('is_admin',)


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','real_name', )}
         ),
    )

    filter_horizontal = ()'''


admin.site.register(MyUser)#,MyUserAdmin)
admin.site.register(Processes)