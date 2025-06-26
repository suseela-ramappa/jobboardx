from django import forms
from .models import Job, Application, JobCategory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class JobForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=JobCategory.objects.all(),
        required=True,
        empty_label='Select a Category',
        label='Category'
    )

    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'job_type', 'category', 'salary', 'requirements', 'benefits']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Post_Job'))

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Apply'))

class JobSearchForm(forms.Form):
    JOB_TYPE_CHOICES = [
        ('', 'Any Type'),
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
    ]
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Job title, keywords, or company'})
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'City, state, or zip code'})
    )
    job_type = forms.ChoiceField(
        choices=JOB_TYPE_CHOICES,
        required=False,
        label='Job Type'
    )
    category = forms.ModelChoiceField(
        queryset=JobCategory.objects.all(),
        required=False,
        empty_label='Any Category',
        label='Category'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap4/layout/inline_field.html'
        self.helper.add_input(Submit('submit', 'Search'))