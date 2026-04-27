from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import CustomerProfile, ProviderProfile

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'user_type', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)

        # Manually assign extra fields
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        user.user_type = self.cleaned_data.get('user_type')

        if commit:
            user.save()

        return user
    
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['first_name', 'last_name', 'phone', 'address', 'bio']


class ProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = ['first_name', 'last_name', 'phone', 'address', 'bio']