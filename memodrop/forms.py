from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, CharField, HiddenInput
from . import models

class RegisterUser(UserCreationForm):
    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
class ColorForm(ModelForm):
    class Meta:
        model = models.User
        fields = ['profile_color']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['form_type'] = CharField(
            initial='color',
            widget=HiddenInput()
        )


class ProfilePicForm(ModelForm):
    class Meta:
        model = models.User
        fields = ['profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['form_type'] = CharField(
            initial='picture',
            widget=HiddenInput()
        )