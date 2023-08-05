from django import forms
from django.conf import settings
from slock.models import BasicUser
from traceback import print_exc
from django.db import models
from django.db.models import Q

class LoginForm(forms.Form):
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, session=None, *args, **kwargs):
        self.session = session
        self.user    = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(LoginForm, self).clean()

        email    = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        ERROR0   = 'User or password is wrong!'
        query    = Q(email = email, password=password)

        # When the user exists it is saved in order to be
        # authenticated later.

        try:
            self.user = BasicUser.objects.get(query)
        except BasicUser.DoesNotExist as e:
            print_exc()
            raise forms.ValidationError(ERROR0)

    def authenticate(self):
        self.session['user_id'] = self.user.id

class SetPasswordForm(forms.ModelForm):
    retype   = forms.CharField(required=True, widget=forms.PasswordInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    def clean(self):
        super(SetPasswordForm, self).clean()
        retype   = self.cleaned_data.get('retype')
        password = self.cleaned_data.get('password')

        if retype != password:
            raise forms.ValidationError(
                'Passwords dont match!')

    class Meta:
        model  = BasicUser
        fields = ('password', )

class UpdatePasswordForm(SetPasswordForm):
    old = forms.CharField(required=True, widget=forms.PasswordInput())
    def clean(self):
        super(UpdatePasswordForm, self).clean()
        old = self.cleaned_data.get('old')
        
        if old != self.instance.password:
            raise forms.ValidationError("Wrong existing password!")




