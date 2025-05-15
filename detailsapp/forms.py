from django import forms
from detailsapp.models import FresherApplicant, ExperiencedApplicant

def validate_file_size(file):
    if file.size > 5 * 1024 * 1024:
        raise forms.ValidationError("File size must be under 5MB.")

def validate_email(value):
    if "@" not in value or not value.endswith(".com"):
        raise forms.ValidationError("Enter a valid email ending with .com")

class FresherForm(forms.ModelForm):
    class Meta:
        model = FresherApplicant
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get("email")
        validate_email(email)
        return email

    def clean_mobile_number(self):
        mobile = self.cleaned_data.get("mobile_number")
        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return mobile

    def clean(self):
        for field in self.files:
            validate_file_size(self.files[field])

class ExperiencedForm(FresherForm):
    class Meta:
        model = ExperiencedApplicant
        fields = '__all__'
