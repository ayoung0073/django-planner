from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=15)

class Daily(models.Model):
    writer = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, default=1)
    date = models.DateField()
    category = models.CharField(max_length = 20, null=True, default = None)
    content = models.CharField(max_length=50, null = True, default = None)
    check = models.IntegerField(null=True, default = None)

    # def __str__(self): # 관리자 페이지에 출력될 내용 설정
    #     return [self.id ,self.name, self.email]
class Diary(models.Model):
    writer = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, default=1)
    date = models.DateField()
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    is_public = models.IntegerField(default = 0) # 0: 나만, 1: 팔로워 가능, 2: public
    
# import된 models.Model을 매개변수로 받고, 
# author : 작성자, ForeignKey는 새로 import한 User 객체를 지정

class Monthly(models.Model): #`id`, `content`, `writer`, `date`
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1)
    date = models.DateField()
    content = models.CharField(max_length=40, null = True, default = None)
    


class Neighbor(models.Model):
    following = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1, related_name='followed')
    following_date = models.DateTimeField(auto_now_add=True) # 해당 레코드 생성시 현재 시간 자동




