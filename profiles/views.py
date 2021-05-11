from django.views.generic import DetailView
from django.contrib.auth.models import User
# Create your views here.

class ProfileDetailView(DetailView):
    template_name = "profiles/detail.html"
    model = User
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"