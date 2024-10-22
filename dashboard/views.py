from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'  # Specify the template name

    # Optionally, you can customize the login URL and redirect URL if needed
    # login_url = 'dashboard/'  
    # redirect_field_name = ''  
