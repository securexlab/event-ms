from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['company_name', 'owner_first_name', 'owner_last_name', 'contact', 'email', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }