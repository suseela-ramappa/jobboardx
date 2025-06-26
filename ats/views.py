
from django.shortcuts import render
from .forms import ATSAnalyzerForm
from .utils import extract_text_from_pdf, calculate_ats_score

def ats_analyzer_view(request):
    score = None
    if request.method == 'POST':
        form = ATSAnalyzerForm(request.POST, request.FILES)
        if form.is_valid():
            resume = request.FILES['resume']
            job_desc = form.cleaned_data['job_description']
            text = extract_text_from_pdf(resume)
            score = calculate_ats_score(text, job_desc)
    else:
        form = ATSAnalyzerForm()
    return render(request, 'ats/analyze.html', {'form': form, 'score': score})
