from django.shortcuts import render, redirect
from .forms import FresherForm, ExperiencedForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FresherApplicant, ExperiencedApplicant
from django.db.models import Q

# Admin Login
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'admin.html')

# Admin Dashboard
@login_required
def admin_dashboard(request):
    search_query = request.GET.get('search')
    fresher_applicants = FresherApplicant.objects.all()
    experienced_applicants = ExperiencedApplicant.objects.all()

    if search_query:
        fresher_applicants = fresher_applicants.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(mobile_number__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(submitted_at__icontains=search_query)
        )
        experienced_applicants = experienced_applicants.filter(
            Q(full_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(mobile_number__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(submitted_at__icontains=search_query)
        )

    applicants = list(fresher_applicants) + list(experienced_applicants)
    return render(request, 'admin.html', {'applicants': applicants})

# Delete Applicant
@login_required
def delete_applicant(request, id):
    FresherApplicant.objects.filter(id=id).delete()
    ExperiencedApplicant.objects.filter(id=id).delete()
    return redirect('admin_dashboard')

# Admin Logout
@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# Fresher Form View
def fresher_view(request):
    if request.method == "POST":
        form = FresherForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            if (FresherApplicant.objects.filter(email=email).exists() or 
                ExperiencedApplicant.objects.filter(email=email).exists()):
                messages.error(request, "This email has already been used to apply.")
            else:
                form.save()
                return redirect('submit_success')
    else:
        form = FresherForm()
    return render(request, "fresher_form.html", {"form": form})


# Experienced Form View
def experienced_view(request):
    if request.method == "POST":
        form = ExperiencedForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            if (FresherApplicant.objects.filter(email=email).exists() or 
                ExperiencedApplicant.objects.filter(email=email).exists()):
                messages.error(request, "This email has already been used to apply.")
            else:
                form.save()
                return redirect('submit_success')
    else:
        form = ExperiencedForm()
    return render(request, "experienced_form.html", {"form": form})


# Submit Success Page
def submit_success(request):
    return render(request, 'submit.html')
