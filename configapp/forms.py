from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from .models import User, Student, Teacher


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="Parol", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Parolni tasdiqlang", widget=forms.PasswordInput)
    ROLE_CHOICES = [
        ('student', 'O‘quvchi'),
        ('teacher', 'Ustoz'),
        ('admin', 'Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Rolni tanlang")

    class Meta:
        model = User
        fields = ['email', 'phone_number']

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Parollar bir xil emas!")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        role = self.cleaned_data.get("role")


        if role == "student":
            user.is_student = True
        elif role == "teacher":
            user.is_teacher = True
        elif role == "admin":
            user.is_admin = True
            user.is_staff = True
            user.is_superuser = True

        if commit:
            user.save()


            if user.is_student:
                Student.objects.create(user=user, full_name=user.email)
            elif user.is_teacher:
                Teacher.objects.create(user=user, full_name=user.email)


            subject = "Ro‘yxatdan o‘tish muvaffaqiyatli"
            message = f"Assalomu alaykum! Siz ERP tizimida ro‘yxatdan o‘tdingiz.\nEmail: {user.email}\nRahmat!"
            send_mail(subject, message, None, [user.email])

        return user



class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Parol", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Email yoki parol noto‘g‘ri!")
            elif not user.is_active:
                raise forms.ValidationError("Bu foydalanuvchi faol emas!")
        return cleaned_data



class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Parol", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Parolni tasdiqlang", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'is_student', 'is_teacher', 'is_admin']

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Parollar mos emas!")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'is_active', 'is_student', 'is_teacher', 'is_admin']
