from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Custom user model
class CustomUser(AbstractUser):
    is_jobseeker = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

# JobSeeker model
class JobSeeker(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

# Employer model
class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
 # ✅ Lazy reference

    def __str__(self):
        return self.user.username

# models.py
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    resume_text = models.TextField(blank=True, null=True)  # To store parsed text
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


