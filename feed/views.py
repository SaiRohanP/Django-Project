#(for function based view)from django.shortcuts import render

from django.views.generic import ListView,DetailView
from .models import Post

# Create your views here.

class HomePage(ListView):
    http_method_names = ["get"]#default
    template_name = "feed/homepage.html"
    model = Post
    context_object_name = "posts"
    queryset = Post.objects.all().order_by('-id')[0:30]

class PostDetailView(DetailView):
    template_name = "feed/detail.html"
    model = Post
    context_object_name = "post"