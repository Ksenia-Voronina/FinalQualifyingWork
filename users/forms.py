from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class RegistrationForm(UserCreationForm):
    """Форма регистрации нового пользователя"""

    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].error_messages = {
            'required': 'Введите пароль',
        }
        self.fields['password2'].error_messages = {
            'required': 'Подтвердите пароль',
        }
        self.fields['username'].help_text = 'Обязательное поле. Только буквы, цифры и символы @/./+/-/_.'
        self.fields['password1'].help_text = 'Пароль должен содержать не менее 8 символов.'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Форма входа в систему (по email или username)"""

    username = forms.CharField(
        label='Логин (email или username)',
        widget=forms.TextInput(attrs={
            'placeholder': 'example@university.ru или username'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages = {
            'required': 'Введите логин',
        }
        self.fields['password'].error_messages = {
            'required': 'Введите пароль',
        }
        # Общее сообщение при неверной аутентификации
        self.error_messages['invalid_login'] = 'Неверный логин или пароль'

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                'Учётная запись не активирована',
                code='inactive',
            )


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля пользователя"""

    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = UserProfile
        fields = ['phone', 'student_id', 'faculty', 'course', 'avatar']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

        self.fields['phone'].error_messages = {
            'invalid': 'Введите корректный номер телефона',
        }
        self.fields['student_id'].error_messages = {
            'invalid': 'Введите корректный номер студенческого билета',
            'max_length': 'Номер студенческого билета должен содержать не более 6 символов',
        }
        self.fields['faculty'].error_messages = {
            'invalid_choice': 'Выберите факультет из списка',
            'required': 'Выберите факультет',
        }
        self.fields['course'].error_messages = {
            'invalid_choice': 'Выберите курс из списка',
            'required': 'Выберите курс',
        }
        self.fields['avatar'].error_messages = {
            'invalid': 'Загрузите корректный файл изображения',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.replace('+', '').replace(' ', '').replace('-', '').replace('(', '').replace(')', '').isdigit():
            raise forms.ValidationError('Номер телефона должен содержать только цифры и символы +, -, (, ), пробел')
        return phone

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if student_id and not student_id.isdigit():
            raise forms.ValidationError('Номер студенческого билета должен содержать только цифры')
        return student_id

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.exclude(id=self.user.id).filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    def save(self, commit=True):
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        return super().save(commit)