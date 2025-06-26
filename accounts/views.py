from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from jobs.models import Company,Application, Job 
from .forms import UserRegisterForm, JobSeekerProfileForm, EmployerProfileForm
from .models import JobSeeker, Employer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            if form.cleaned_data.get('is_jobseeker'):
                user.is_jobseeker = True
            elif form.cleaned_data.get('is_employer'):
                user.is_employer = True

            user.save()

            if user.is_jobseeker:
                JobSeeker.objects.create(user=user)

            if user.is_employer:
                company_name = form.cleaned_data.get('company_name')
                company_description = form.cleaned_data.get('company_description')
                company_website = form.cleaned_data.get('company_website')

                # ✅ Try to find an existing company (don't overwrite the Company class!)
                existing_company = Company.objects.filter(
                    name=company_name,
                    website=company_website
                ).first()

                if existing_company:
                    company = existing_company
                else:
                    company = Company.objects.create(
                        name=company_name,
                        description=company_description,
                        website=company_website,
                        created_by=user
                    )

                # ✅ Create employer and link to the found or new company
                Employer.objects.create(user=user, company=company)

            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_jobseeker:
        return redirect('jobseeker_dashboard')
    elif request.user.is_employer:
        return redirect('employer_dashboard')
    else:
        return redirect('home')

@login_required
def jobseeker_dashboard(request):
    if not request.user.is_jobseeker:
        return redirect('home')

    jobseeker = request.user.jobseeker
    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=jobseeker)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('jobseeker_dashboard')
    else:
        form = JobSeekerProfileForm(instance=jobseeker)

    return render(request, 'accounts/jobseeker_dashboard.html', {
        'form': form,
        'jobseeker': jobseeker,
    })
@login_required
def employer_dashboard(request):
    if not request.user.is_employer:
        return redirect('home')

    employer = request.user.employer  # get Employer instance

    # ✅ Fixed: use employer instance instead of request.user
    recent_applications = Application.objects.filter(
        job__employer=employer
    ).order_by('-applied_at')[:5]

    active_jobs = Job.objects.filter(
        employer=employer,
        is_active=True
    ).order_by('-created_at')

    active_jobs_count = Job.objects.filter(is_active=True).count()
    total_applications = Application.objects.all().count()

   
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, instance=employer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('employer_dashboard')
    else:
        form = EmployerProfileForm(instance=employer)

    return render(request, 'accounts/employer_dashboard.html', {
        'form': form,
        'employer': employer,
        'recent_applications': recent_applications,
        'active_jobs': active_jobs,
        'active_jobs_count': active_jobs_count,
        'total_applications': total_applications,
        
    })


def logout_view(request):
    logout(request)
    return redirect('login')
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def extract_keywords(text, top_n=10):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return list(set(words))[:top_n]

def recommended_jobs_view(request):
    user = request.user
    user_profile = getattr(user, 'profile', None)
    recommended_jobs = Job.objects.none()

    if user_profile and user_profile.resume_text:
        resume_keywords = extract_keywords(user_profile.resume_text)
        if resume_keywords:
            jobs = Job.objects.filter(is_active=True)
            job_texts = [f"{job.title} {job.location} {job.get_job_type_display()}" for job in jobs]

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(job_texts + [' '.join(resume_keywords)])
            similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

            # Sort jobs by similarity score
            scored_jobs = sorted(zip(similarities[0], jobs), reverse=True)
            recommended_jobs = [job for score, job in scored_jobs[:5] if score > 0.1]  # Threshold

    else:
        # fallback to recent jobs
        recommended_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:5]

    return render(request, 'dashboard.html', {
        'recommended_jobs': recommended_jobs,
    })
