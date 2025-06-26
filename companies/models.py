from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField()
    logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)  # ✅ Lazy reference

    def __str__(self):
        return self.name

