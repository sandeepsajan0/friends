from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import PostForm, Post, RegistrationForm, GroupForm, Group
from django.views.generic import TemplateView
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from django.contrib.auth.models import User

# Create your views here.
def firstview(request):
    return render(request, 'base.html')

@login_required
def HomePage(request):
    groups = Group.objects.filter(users=request.user)
    return render(request, 'main.html',{'groups':groups})

def show_groups(request,pk=None):
    group = Group.objects.get(pk=pk)
    print(group.name)
    return render(request, 'group.html',{'group':group})

@login_required
def CreateGroup(request):
    template_name = "create_group.html"
    form = GroupForm()
    if request.method=='POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            gp = form.save(commit=False)
            gp.save()
            gp.users.add(request.user)
            gp.save()
            form = GroupForm()
    return render(request,template_name,{'form':form})


@login_required
def add_member(request):
    template_name = "add_member.html"
    if request.method=='POST':
        gp_name = request.POST.get('gp_name',None)
        member = request.POST.get('member',None)
        group = Group.objects.get(name=gp_name)
        user_name=User.objects.get(username=member)
        group.users.add(user_name)
        return redirect('/friends/user/group/add_member/')
    else:
        return render(request,template_name)
    

@login_required
def openMessages(request):
    template_name='open_posts.html'
    
    form = PostForm()

    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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

