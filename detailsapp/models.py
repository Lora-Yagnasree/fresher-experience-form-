from django.db import models

def upload_path(instance, filename):
    return f'documents/{instance.full_name}/{filename}'

class ApplicantBase(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=10)
    address = models.TextField()

    ssc_memo = models.FileField(upload_to=upload_path)
    inter_memo = models.FileField(upload_to=upload_path)
    degree_memo = models.FileField(upload_to=upload_path)
    aadhar_card = models.FileField(upload_to=upload_path)
    pan_card = models.FileField(upload_to=upload_path)
    passport_photo = models.FileField(upload_to=upload_path)

    submitted_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation

    class Meta:
        abstract = True

    def __str__(self):
        return self.full_name

class FresherApplicant(ApplicantBase):
    pass

class ExperiencedApplicant(ApplicantBase):
    pre_offer_letter = models.FileField(upload_to=upload_path, null=True, blank=True)
    pay_slips = models.FileField(upload_to=upload_path, null=True, blank=True)
    relieving_experience = models.FileField(upload_to=upload_path, null=True, blank=True)
