from django import forms
from MainApp.models import Snippet

from django.contrib.auth.models import User


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ["name", "lang", "code", "description", "public"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название сниппета'}),
            'lang': forms.Select(attrs={'class': 'form-control'}),
            'code': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Код сниппета'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание сниппета'}),
            'public': forms.CheckboxInput(attrs={'class': 'custom-checkbox'}),
        }

    # Пример валидации на уровне поля (опционально)
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError("Название должно содержать не менее 3 символов.")
        return name

    # Пример валидации на уровне формы (опционально)
    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        description = cleaned_data.get('description')

        if code and len(code) < 10 and not description:
            # Если код очень короткий, а описание отсутствует, добавить ошибку
            self.add_error(None, "Для очень короткого кода требуется описание.")  # Общая ошибка формы
        return cleaned_data


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
        }

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password'})
    )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'confirm password'})
    )

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 == password2:
            return password2
        raise forms.ValidationError("Пароли пустые или не совпадают")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
# class SnippetForm(forms.Form):
#     name = forms.CharField(
#         label = '',
#         # label="Название сниппета",
#         required=True,
#         max_length=100,
#         widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Краткое название"}),
#     )
#
#     lang = forms.ChoiceField(
#         label = '',
# #         label="Язык программирования",
#         choices=[
#             ('', '--- Выберите язык ---'),
#             ("python", "Python"),
#             ("cpp", "C++"),
#             ("java", "Java"),
#             ("javascript", "JavaScript")
#         ],
#         required=True,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#
#     code = forms.CharField(
#         label = '',
# #         label="Исходный код",
#         max_length=5000,
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Введите ваш код здесь'})
#     )
