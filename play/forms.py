from django import forms


class NumForm(forms.Form):
    number = forms.IntegerField(label='Введите загаданное число', max_value=99, min_value=10)
