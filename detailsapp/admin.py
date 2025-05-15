from django.contrib import admin
from .models import FresherApplicant, ExperiencedApplicant

@admin.register(FresherApplicant)
class FresherApplicantAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'email', 'mobile_number',
        'ssc_memo', 'inter_memo', 'degree_memo',
        'aadhar_card', 'pan_card', 'passport_photo'
    )
    search_fields = ('full_name', 'email', 'mobile_number')

@admin.register(ExperiencedApplicant)
class ExperiencedApplicantAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'email', 'mobile_number', 'relieving_experience',
        'ssc_memo', 'inter_memo', 'degree_memo',
        'aadhar_card', 'pan_card', 'passport_photo',
        'pre_offer_letter', 'pay_slips'
    )
    search_fields = ('full_name', 'email', 'mobile_number', 'relieving_experience')

# Register your models here.
