from django import forms


class TestForm(forms.Form):
    login = forms.CharField(label="Логин", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    group_id = forms.IntegerField()