from django.db import models
import os
from django.contrib.auth.models import User
#from django.contrib.auth import models
# Create your models here.

# def get_upload_file_name(instance,filename):
#     #print instance.author
#     return "uploads/%s/%s" % (instance.user_name,filename)
# def dummy_function(instance,filename):
#     #print instance.author
#     return
def get_upload_file_name(self,filename):
    print 'get_upload_file_name',self.question,filename
    return "uploads/%s/%s" % (self.question,filename)
class Question(models.Model):
    question = models.CharField(max_length=200)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    image = models.ImageField(upload_to=get_upload_file_name,default='00000')
    option_correct = models.CharField(max_length=2)
    file_path = models.CharField(max_length=200,default='00000')
    class Meta:
        db_table='questions'

class Answer(models.Model):
    user_name = models.CharField(max_length=500)
    question_id = models.CharField(max_length=2)
    answer = models.CharField(max_length=2)
    class Meta:
        db_table='answer'
class Reposted_Answer(models.Model):
    user_name = models.CharField(max_length=500)
    question_id = models.CharField(max_length=2)
    answer = models.CharField(max_length=2)
    class Meta:
        db_table='reposted_answer'
class Posted_Question(models.Model):
    question_id = models.CharField(max_length=2)
    number_of_times=models.CharField(max_length=2)
    class Meta:
        db_table='published_questions'


#class Request_recv(models.Model):
    #user_name= models.CharField(max_length=200,default='00000')
    #friend_req= models.CharField(max_length=200,default='00000')