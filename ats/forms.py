from django import forms

class ATSAnalyzerForm(forms.Form):
    resume = forms.FileField(label="Upload Resume (PDF only)")
    job_description = forms.CharField(widget=forms.Textarea, label="Paste Job Description")
