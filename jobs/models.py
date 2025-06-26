from django.db import models
from django.contrib.auth import get_user_model
from companies.models import Company
from accounts.models import Employer

User = get_user_model()

class JobCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Job(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    salary = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('reviewed', 'Reviewed'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='application_resumes/')

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"