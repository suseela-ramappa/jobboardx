from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Company
from .forms import CompanyForm
from django.contrib import messages

@login_required
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.created_by = request.user
            company.save()
            messages.success(request, 'Company created successfully!')
            return redirect('employer_dashboard')
    else:
        form = CompanyForm()
    return render(request, 'companies/create_company.html', {'form': form})
# companies/views.py
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'companies/company_list.html', {'companies': companies})
