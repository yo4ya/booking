from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Schedule
from django import forms

User = get_user_model()  # Userモデルの柔軟な取得方法


class UserCreateForm(forms.ModelForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = Schedule
        fields = ('name', 'number', 'tel',)  # ユーザー名として扱っているフィールドだけ、作成時に入力する

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            