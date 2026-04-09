from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Item, UserProfile
 
 
class CustomRegistrationForm(UserCreationForm):
    email          = forms.EmailField(required=False)
    first_name     = forms.CharField(max_length=100, required=False)
    last_name      = forms.CharField(max_length=100, required=False)
    role           = forms.CharField(max_length=100, required=False,
                                     help_text="e.g. Student, Faculty, Staff")
    contact_number = forms.CharField(max_length=20, required=False)
 
    class Meta:
        model  = User
        fields = ['username', 'email', 'first_name', 'last_name',
                  'role', 'contact_number', 'password1', 'password2']
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email      = self.cleaned_data.get('email', '')
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name  = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            # Save extra fields to profile
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role           = self.cleaned_data.get('role', '')
            profile.contact_number = self.cleaned_data.get('contact_number', '')
            profile.save()
        return user
 
 
class ItemForm(forms.ModelForm):
    class Meta:
        model  = Item
        fields = ['title', 'description', 'status', 'category',
                  'location', 'date_lost_found', 'photo']
        widgets = {
            'date_lost_found': forms.DateInput(attrs={'type': 'date'}),
            'description':     forms.Textarea(attrs={'rows': 4}),
        }