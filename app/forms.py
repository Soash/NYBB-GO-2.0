import random
import string
from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from django.conf import settings

def generate_random_password(length=8):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def generate_unique_username(first_name):
    base_username = ''.join(filter(str.isalpha, first_name)).lower()
    username = base_username
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{random.randint(1000, 9999)}"
    return username

class SignUpForm(forms.ModelForm):
    full_name = forms.CharField(label="Full Name", max_length=100)
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ('full_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Store the full name in first_name and leave last_name blank
        user.first_name = self.cleaned_data.get('full_name')
        user.last_name = ''

        user.username = generate_unique_username(user.first_name)
        password = generate_random_password()
        user.set_password(password)

        if commit:
            user.save()
            try:
                send_mail(
                    'Your account credentials',
                    f'Welcome to NYBB Go!\nUsername: {user.username}\nPassword: {password}',
                    settings.DEFAULT_FROM_EMAIL,
                    [self.cleaned_data.get('email')],
                    fail_silently=False,
                )
            except BadHeaderError:
                print("Invalid header found. Email not sent.")
            except Exception as e:
                print(f"An error occurred: {e}. Email not sent.")
        return user


