from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    DCode = models.IntegerField(primary_key=True)
    DName = models.CharField(max_length=20)
    Ddes = models.CharField(max_length=100)
    Dinfo = models.CharField(max_length=3000)
    ImgLink = models.ImageField(upload_to="departments", default="")

    def __str__(self):
        return self.DName


class Course(models.Model):
    CCode = models.CharField(primary_key=True, max_length=20)
    CName = models.CharField(max_length=200)
    CDes = models.CharField(max_length=3000)
    DCode = models.ForeignKey(Department, on_delete=models.CASCADE)


class Uploader(models.Model):
    UNumber = models.AutoField(primary_key=True)
    UName = models.CharField(max_length=50)


class Resource(models.Model):
    RNo = models.AutoField(primary_key=True)
    RName = models.CharField(max_length=100)
    RDes = models.CharField(max_length=200)
    CCode = models.ForeignKey(Course, on_delete=models.CASCADE)
    UNumber = models.ForeignKey(Uploader, on_delete=models.CASCADE)
    filepath = models.FileField(upload_to="resources", default="")


class Request(models.Model):
    ReqNo = models.AutoField(primary_key=True)
    RDes = models.CharField(max_length=200)
    Userno = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    Name = models.CharField(max_length=30)
    Email = models.CharField(max_length=50)
    Subject = models.CharField(max_length=200)
    Feedback = models.CharField(max_length=2000)
