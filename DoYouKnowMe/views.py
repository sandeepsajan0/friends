from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import PostForm, Post, RegistrationForm, GroupForm, Group
from django.views.generic import TemplateView
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime
from django.contrib.auth.models import User

from rest_framework import status
from django.contrib.auth import authenticate,login,logout 
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import PostSerializer,PostPutSerializer,RegisterSerializer

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
    form = PostForm()
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid():
            curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            items = form.save(commit = False)
            items.author = request.user
            items.author_name = request.user.username
            items.date_added = curr_time
            items.group_name = group.name
            items.save()
            form = PostForm()
    context={}
    context["posts"] = Post.objects.filter(group_name=group.name)
    object_list=context["posts"]
    return render(request,'group.html', {'object_list':context["posts"], 'form': form, 'group':group})


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
            items.group_name = "Open"
            items.save()
            form = PostForm()
    context={}
    context["posts"] = Post.objects.filter(group_name="Open")
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



"""  ********* Backend APIs **********  """

class Login_View(APIView):
    model = User
    def post(self,request,format=None):
        data = request.data
        print(data)
        username = data.get('username', None)
        password = data.get('password', None)
        print(username)
        user = authenticate(request,username=username, password=password)
        print (user)
        if user is not None:
            if user.is_active:
                login(request, user)
                print(request.user)
                print("done!")
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Logout_View(APIView):
    def get(self,request):
        print(request.user)
        logout(request)
        return HttpResponse("logout")
            

class ProfileView(APIView):
    model = User
    def get(self,request):
        queryset = list(User.objects.filter(username= request.user.username).values('username','first_name','last_name','email'))
        return JsonResponse(queryset,safe = False)

class RegisterUser(APIView):
     model = User
     def post(self,request,format='json'):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            registered_user= serializer.save()
            print(serializer.data)
        return Response({"user:":serializer.data})

class OpenPostAdd(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    model = Post
    serializer_class = PostPutSerializer
    def perform_create(self, serializer):
        instance = self.model(**serializer.validated_data)
        instance.group_name = 'Open'
        instance.save()

class OpenPostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        return Post.objects.all()
