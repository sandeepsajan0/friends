from rest_framework import serializers
from .models import Post
from django import forms
from django.contrib.auth.models import User

class PostSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Post
        fields = ('id','author_name','text','date_added','group_name')
        extra_kwargs = {
            'url': {
                'view_name': 'post_detail',
            }
        }
        

class PostPutSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('text',)
        
        extra_kwargs = {
            'url': {
                'view_name': 'post_add',
            }
        }
        
class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    email = forms.EmailField(required = True,help_text='Required')
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)

