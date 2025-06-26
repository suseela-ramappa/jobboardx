from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, JobSeeker, Employer
from companies.models import Company


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    is_jobseeker = forms.BooleanField(required=False, label="Register as Job Seeker")
    is_employer = forms.BooleanField(required=False, label="Register as Employer")

    # Employer-specific fields
    company_name = forms.CharField(max_length=100, required=False)
    company_description = forms.CharField(widget=forms.Textarea, required=False)
    company_website = forms.URLField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2',
            'is_jobseeker', 'is_employer',
            'company_name', 'company_description', 'company_website'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.is_jobseeker = self.cleaned_data.get('is_jobseeker', False)
        user.is_employer = self.cleaned_data.get('is_employer', False)

        if commit:
            user.save()

            if user.is_jobseeker:
                JobSeeker.objects.create(user=user)

            if user.is_employer:
                company_name = self.cleaned_data.get('company_name')
                company_description = self.cleaned_data.get('company_description')
                company_website = self.cleaned_data.get('company_website')

                # Check if a company with the same name and website exists
                company = Company.objects.filter(
                    name=company_name,
                    website=company_website
                ).first()

                # If not found, create a new one
                if not company:
                    company = Company.objects.create(
                        name=company_name or "Default Company",
                        description=company_description or "No description provided.",
                        website=company_website or "https://example.com",
                        created_by=user
                    )

                # Link employer to the company
                Employer.objects.create(user=user, company=company)

        return user


class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['resume', 'skills', 'experience', 'education']


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company']
