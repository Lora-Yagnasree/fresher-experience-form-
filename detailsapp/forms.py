from django import forms
from detailsapp.models import FresherApplicant, ExperiencedApplicant

# Utility to validate email format
def validate_email(value):
    if "@" not in value or not value.endswith(".com"):
        raise forms.ValidationError("Enter a valid email ending with .com")

# Utility to validate individual file size
def validate_file_size(file):
    if file.size > 5 * 1024 * 1024:  # 5MB
        raise forms.ValidationError("File size must be under 5MB.")

# -------------------------
# Fresher Form
# -------------------------
class FresherForm(forms.ModelForm):
    class Meta:
        model = FresherApplicant
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get("email")
        validate_email(email)

        # Check uniqueness across Fresher and Experienced applicants
        from detailsapp.models import ExperiencedApplicant
        if FresherApplicant.objects.filter(email=email).exists() or ExperiencedApplicant.objects.filter(email=email).exists():
            raise forms.ValidationError("This email has already been used to apply.")
        return email

    def clean_mobile_number(self):
        mobile = self.cleaned_data.get("mobile_number")
        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return mobile

    def clean(self):
        cleaned_data = super().clean()
        for field_name, file in self.files.items():
            try:
                validate_file_size(file)
            except forms.ValidationError as e:
                self.add_error(field_name, e)
        return cleaned_data

# -------------------------
# Experienced Form
# -------------------------
class ExperiencedForm(forms.ModelForm):
    class Meta:
        model = ExperiencedApplicant
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get("email")
        validate_email(email)

        # Check uniqueness across Fresher and Experienced applicants
        from detailsapp.models import FresherApplicant
        if FresherApplicant.objects.filter(email=email).exists() or ExperiencedApplicant.objects.filter(email=email).exists():
            raise forms.ValidationError("This email has already been used to apply.")
        return email

    def clean_mobile_number(self):
        mobile = self.cleaned_data.get("mobile_number")
        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return mobile

    def clean(self):
        cleaned_data = super().clean()
        for field_name, file in self.files.items():
            try:
                validate_file_size(file)
            except forms.ValidationError as e:
                self.add_error(field_name, e)
        return cleaned_data
