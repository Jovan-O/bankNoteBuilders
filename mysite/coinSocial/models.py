from django.db import models
from django.contrib.auth.models import User

# database portion
# Create your models here.


# class User(models.Model):
#     userID = models.IntegerField(primary_key=1)
#     profilePicUG = models.ImageField(upload_to='profilePic/')
#     userType = models.BooleanField(default=0)    # unless admin, admin gets 1
#     descriptionUG = models.CharField(max_length=450)
#  might add number of post later

# @User.register() create overloading for user pics
# class UserPic(User.Model)


class Collector(models.Model):
    # all user generated so drop naming convention
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # got set null error, cascading for now
    # set null should let us keep child records
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.CharField(max_length=30)

    def __str__(self):
        return f'Collector name: {self.user} and Collector email {self.email}'


class AdminRole(models.IntegerChoices):
    superAdmin = 1,
    moderator = 2,
    contentCreator = 3,


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # got set null error, cascading for now
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    role = models.IntegerField(choices=AdminRole.choices, default=AdminRole.moderator)
    # for selecting level of admin

    def __str__(self):
        return f'Admin user: {self.user} Admin role: {self.role}'


class ModerationLog(models.Model):
    actionChoices = [
        ('CREATE', 'create'),
        ('EDIT', 'edit'),
        ('DELETE', 'delete'),
        ('BAN', 'ban'),
        ('UNBAN', 'unban'),
    ]
    typeChoices = [
        ('USER', 'user'),
        ('POST', 'post')
        # ('DM', 'message')
    ]

    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='moderationLogs')
    # got set null error, cascading for now
    action = models.CharField(max_length=10, choices=actionChoices)
    timestamp = models.DateTimeField(auto_now_add=1)
    type = models.CharField(max_length=10, choices=typeChoices)  # description of type, could be user or post
    notesUG = models.TextField(blank=1, null=1)

    def __str__(self):
        return f"{self.action} by {self.admin} on {self.timestamp}"


class Collection(models.Model):
    collectionID = models.AutoField(primary_key=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    nameUG = models.CharField(max_length=30)
    descriptionUG = models.CharField(max_length=450)
    publicUG = models.BooleanField(default=0)  # archive will be 1

    def __str__(self):
        return f'Collection: {self.nameUG} and Owner: {self.owner}'


class Item(models.Model):
    # all user generated so no need for convention
    conditionChoices = [
        ('MINT', 'mint'),
        ('GOOD', 'good'),
        ('NORMAL', 'normal'),
        ('POOR', 'poor')
    ]
    id = models.AutoField(primary_key=1)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=1)
    value = models.IntegerField(default=0, null=1)
    condition = models.CharField(max_length=10, choices=conditionChoices, default='Normal')
    origin = models.CharField(max_length=30, null=1)
    description = models.TextField(blank=1, null=1)  # optional
    dateOfIssue = models.DateTimeField("date of Issue", default="Unknown")
    # ideally would love to implement a feature that allows users to select the date range of a coin
    frontImg = models.ImageField(upload_to='moneyPhotos/front/')
    backImg = models.ImageField(upload_to='moneyPhotos/back/')

    def __str__(self):
        return f'Item: {self.id} name: {self.name} condition: {self.condition}'


class Post(models.Model):
    postID = models.AutoField(primary_key=1)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    createdTime = models.DateTimeField(auto_now_add=1)
    editedTime = models.DateTimeField(auto_now=1)

    def __str__(self):
        return f'Post {self.postID} by {self.user}'
