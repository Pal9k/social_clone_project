# that returns a user model that currently active in this project
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserCreateFrom(UserCreationForm):

    class Meta:
        fields = ('username','email','password1','password2')
        model = get_user_model()

    # as we used inbuilt from django and if we want to change the label of fields below is what you can do
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = "Email Address"
