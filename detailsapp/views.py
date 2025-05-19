from django.shortcuts import render, redirect
from .forms import FresherForm, ExperiencedForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FresherApplicant, ExperiencedApplicant
from django.db.models import Q
from itertools import chain
from operator import attrgetter
from datetime import datetime, date

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
    search_query = request.GET.get('search', '').strip()
    date_filter = request.GET.get('date', '').strip()
    month_filter = request.GET.get('month', '').strip()

    fresher_applicants = FresherApplicant.objects.all()
    experienced_applicants = ExperiencedApplicant.objects.all()

    # Unique Dates
    fresher_dates = fresher_applicants.values_list('submitted_at__date', flat=True).distinct()
    experienced_dates = experienced_applicants.values_list('submitted_at__date', flat=True).distinct()
    unique_dates = sorted(set(fresher_dates) | set(experienced_dates), reverse=True)

    # Unique Months (YYYY-MM)
    fresher_months = {dt.strftime("%Y-%m") for dt in fresher_applicants.values_list('submitted_at', flat=True) if dt}
    experienced_months = {dt.strftime("%Y-%m") for dt in experienced_applicants.values_list('submitted_at', flat=True) if dt}
    unique_month_strs = fresher_months | experienced_months
    unique_months = [date(int(m.split('-')[0]), int(m.split('-')[1]), 1) for m in unique_month_strs]
    unique_months.sort(reverse=True)

    # Apply Search Filter
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

    # Apply Date Filter
    selected_date = None
    if date_filter:
        try:
            selected_date = datetime.strptime(date_filter, "%Y-%m-%d").date()
            fresher_applicants = fresher_applicants.filter(submitted_at__date=selected_date)
            experienced_applicants = experienced_applicants.filter(submitted_at__date=selected_date)
        except ValueError:
            selected_date = None

    # Apply Month Filter
    selected_month = None
    if month_filter:
        try:
            filter_year, filter_month = map(int, month_filter.split('-'))
            fresher_applicants = fresher_applicants.filter(
                submitted_at__year=filter_year,
                submitted_at__month=filter_month
            )
            experienced_applicants = experienced_applicants.filter(
                submitted_at__year=filter_year,
                submitted_at__month=filter_month
            )
            selected_month = month_filter
        except ValueError:
            selected_month = None

    # Combine and sort all applicants
    all_applicants = list(chain(fresher_applicants, experienced_applicants))
    all_applicants_sorted = sorted(all_applicants, key=attrgetter('submitted_at'), reverse=True)

    context = {
        'applicants': all_applicants_sorted,
        'unique_dates': unique_dates,
        'unique_months': unique_months,
        'selected_date': date_filter,
        'selected_month': month_filter,
        'search_query': search_query,
    }
    return render(request, 'admin.html', context)

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
            if FresherApplicant.objects.filter(email=email).exists() or ExperiencedApplicant.objects.filter(email=email).exists():
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
            if FresherApplicant.objects.filter(email=email).exists() or ExperiencedApplicant.objects.filter(email=email).exists():
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














   
