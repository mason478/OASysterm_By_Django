from django import forms


class LoginForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput(
        attrs={'placeholder': 'Please enter your username',
               'class':'form-control name-body'}))
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Please enter your password',
                                          'class':'form-control passwd-body'}))
    rememberme=forms.BooleanField(label="Remember me",required=False)