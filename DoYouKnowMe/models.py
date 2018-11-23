from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,default =1)
    text = models.CharField(max_length=500)
    date_added = models.DateTimeField('date published', default=timezone.now)
    author_name = models.CharField(max_length=200,default=author)
    group_name =models.CharField(max_length=100,default=None,blank=True)
    def get_absolute_url(self):
	    return reverse('post_list')
    
    def __unicode__(self):
        return u'%s %s %s %s %s' % (self.text, self.date_added,self.author,self.author_name,self.group_name)


    
class Group(models.Model):
    name=models.CharField(max_length=200)
    users = models.ManyToManyField(User)



class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ("name",)


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("text",)


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required = True,help_text='Required')
	
	class Meta:
		model = User
		fields = (
			"username",
			"first_name",
			"last_name",
			"email",
			"password1",
			"password2"
		)
	
	def save(self,commit = True):
		user = super(RegistrationForm, self).save(commit = False)
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		user.email = self.cleaned_data["email"]
		
		if commit:
			user.save()
		return user
