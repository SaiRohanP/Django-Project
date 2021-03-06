#(for function based view)from django.shortcuts import render

from django.views.generic import TemplateView,DetailView,ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from followers.models import Follower
from .models import Post

# Create your views here.

class HomePage(TemplateView):
    http_method_names = ["get"]#default
    template_name = "feed/homepage.html"
    model = Post
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        if self.request.user.is_authenticated:
            following=list(
                Follower.objects.filter(followed_by=self.request.user).values_list('following',flat=True)
            )
            if following:
                posts=Post.objects.filter(author__in = following).order_by('-id')
            else:
                posts=Post.objects.all().order_by('-id')     
        else:
            posts=Post.objects.all().order_by('-id')
        
        context['posts']=posts
        return context

class PostDetailView(DetailView):
    template_name = "feed/detail.html"
    model = Post
    context_object_name = "post"

class CreatePostView(LoginRequiredMixin,CreateView):
    template_name = "feed/create.html"
    model = Post
    fields = ['text']
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request,*args,**kwargs)

    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()

        return super().form_valid(form)

    def post(self, request, *args, **kwargs):

        post = Post.objects.create(
            text=request.POST.get("text"),
            author=request.user,
        )

        return render(
            request,
            "includes/post.html",
            {
                "post": post,
                "show_detail_link": True,
            },
            content_type="application/html"
        )

class MyPosts(ListView):
    template_name = "feed/myposts.html"
    model = Post
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        posts = Post.objects.filter(author = self.request.user).order_by('-id')
        context['posts']=posts
        return context