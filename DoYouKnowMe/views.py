from django.shortcuts import render
from django.http import HttpResponse
from .models import PostForm, Post
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from time import gmtime, strftime

# Create your views here.
def firstview(request):
    return render(request, 'main.html')

@login_required
def CreateGroup(request):
    return HttpResponse("create gp form")

@login_required
def openMessages(request):
    template_name='open_posts.html'
    
    form = PostForm()

    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            items = form.save(commit = False)
            items.author = request.user
            items.author_name = request.user.username
            items.date_added = curr_time
            items.save()
            form = PostForm()
    context={}
    context["posts"] = Post.objects.all()
    object_list=context["posts"]
    return render(request,'open_posts.html', {'object_list':context["posts"], 'form': form})


class Register(TemplateView):
    template_name = 'registration.html'
    
    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            form = RegistrationForm()
        return render(request,self.template_name,{'form':form})
    def get(self,request):
        form=RegistrationForm()
        return render(request,self.template_name,{'form':form})

class Profile(TemplateView):
    template_name = 'profile.html'
    @method_decorator(login_required)
    def get(self,request):
        return render(request,self.template_name)      
#class openMessages(TemplateView):
#    template_name='open_posts.html'
#    
#    def get(self, request):
#        form=PostForm()
#        return render(request, self.template_name, {'form':form})
#        
#    def post(self, request):
#        form=PostForm(request.POST)
#        if form.is_valid():
#            form.save()
#            form = PostForm()
#        some = Post.objects.all()
#        args = {'form':form, 'some':some}
#        return render(request,self.template_name,args)
#     
