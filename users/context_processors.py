from .models import Profile

def company_name_processor(request):
    company = Profile.objects.first()
    return {
        'company_name': company.company_name if company else ''
    }
