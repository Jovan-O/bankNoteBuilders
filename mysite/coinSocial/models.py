from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models

import string
import random


# database portion
# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=15, unique=1)  # needs a value
    description = models.TextField(null=1, blank=1)

    # def save(self, username, description):
    #     if not username:
    #         name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    #         user = self.model(description=description, username=name)
    #         user.save()
    #         return user
#  might add number of post later


# @User.register() create overloading for user pics
# class UserPic(User.Model)
class Collector(models.Model):
    # all user generated so drop naming convention
    name = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    u = CustomUser.objects.create_user(username=name)

    user = models.OneToOneField(u, on_delete=models.CASCADE, null=1)
    # got set null error, cascading for now
    # set null should let us keep child records
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.CharField(max_length=30, unique=1)

    # def save(self, *args, **kwargs):
    #     u = CustomUser.objects.create(username=name, description='NULL')
    #     self.user = u
    #     self.save()
    #     return self

    def __str__(self):
        return f'Collector name: {self.user} and Collector email {self.email}'


class AdminRole(models.IntegerChoices):
    superAdmin = 3,
    moderator = 2,
    contentCreator = 1,


class Admin(models.Model):
    # q = Admin(user={USER_OBJECT}, firstName="some", lastName="name")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # might need to rework this line
    # got set null error, cascading for now
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    role = models.IntegerField(choices=AdminRole.choices, default=AdminRole.moderator)
    # for selecting level of admin

    def save(self, *args, **kwargs):
        if not self.user:  # Check if the Collector object is being created
            u = CustomUser()
            self.user = u
            self.save()
            return self

    def __str__(self):
        return f'Admin full name: {self.firstName}, {self.lastName} Admin role lvl: {self.role}'


class ModerationLog(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='moderationLogs')
    # got set null error, cascading for now
    action = models.CharField(max_length=10, choices=[
        ('CREATE', 'create'),
        ('EDIT', 'edit'),
        ('DELETE', 'delete'),
        ('BAN', 'ban'),
        ('UNBAN', 'unban'),
    ])
    timestamp = models.DateTimeField(auto_now_add=1)
    type = models.CharField(max_length=10, choices=[
        ('USER', 'user'),
        ('POST', 'post')
        # ('DM', 'message')
    ])  # description of type, could be user or post
    notes = models.TextField(blank=1, null=1)

    def __str__(self):
        return f"{self.action} by {self.admin} on {self.timestamp}"


class Collection(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=450)
    public = models.BooleanField(default=0)  # archive will be 1

    def __str__(self):
        return f'Name of collection: {self.name} and Owner: {self.owner.username} and ID:{self.id}'


class Item(models.Model):
    # all user generated so no need for convention
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=1)
    value = models.IntegerField(default=0, null=1)
    condition = models.CharField(max_length=10, choices=[
        ('MINT', 'mint'),
        ('GOOD', 'good'),
        ('NORMAL', 'normal'),
        ('POOR', 'poor')
    ], default='Normal')
    origin = models.CharField(max_length=30, null=1)
    description = models.TextField(blank=1, null=1)  # optional
    dateOfIssue = models.DateTimeField("date of Issue", null=1, blank=1)
    # ideally would love to implement a feature that allows users to select the date range of a coin
    frontImg = models.ImageField(upload_to='moneyPhotos/front/')
    backImg = models.ImageField(upload_to='moneyPhotos/back/')

    def __str__(self):
        return f'Item: {self.id} name: {self.name} condition: {self.condition}'


class Post(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    createdTime = models.DateTimeField(auto_now_add=1)
    editedTime = models.DateTimeField(auto_now=1)

    def __str__(self):
        return f'Post {self.id} by {self.item.collection.owner.username}'
