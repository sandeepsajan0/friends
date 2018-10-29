from django.contrib import admin
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.firstview),
    url(r'^user/$',views.HomePage),
    url(r'^user/create_group/$',views.CreateGroup),
    url(r'^user/group/(?P<pk>\d+)/$', views.show_groups, name='group'),
    url(r'^user/open_messages/$',views.openMessages, name='post_list'),
    url(r'^register/$',views.Register.as_view()),
    url(r'^login/$',LoginView.as_view(template_name='login.html'),name='login'),
    url(r'^logout/$',LogoutView.as_view(template_name='logout.html')),
    url(r'^user/profile/$',views.Profile.as_view()),
    url(r'^user/group/add_member/$', views.add_member, name="add_member"),
]
