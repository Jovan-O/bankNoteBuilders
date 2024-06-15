from django.db import models
# database portion
# Create your models here.


class User(models.Model):
    userID = models.IntegerField(primary_key=1)
    profilePicUG = models.ImageField(upload_to='profilePic/')
    userType = models.BooleanField(default=0)    # unless admin, admin gets 1
    descriptionUG = models.CharField(max_length=450)
    # might add number of post later


class Collector(models.Model):
    # all user generated so drop naming convention
    user = models.ForeignKey(User, on_delete=models.SET_NULL)  # lets us keep child records
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    email = models.CharField(max_length=30)


class AdminRole(models.IntegerChoices):
    superAdmin = 1,
    moderator = 2,
    contentCreator = 3,


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)  # lets us keep child records
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    role = models.IntegerField(choices=AdminRole.choices, default=AdminRole.moderator)
    # for selecting level of admin





class Collection(models.Model):
    collectionID = models.IntegerField(primary_key=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    nameUG = models.CharField(max_length=30)
    descriptionUG = models.CharField(max_length=450)
    publicUG = models.BooleanField(default=0)  # archive will be 1


class Item(models.Model):
    # all user generated so no need for convention
    frontImg = models.ImageField(upload_to='moneyPhotos/front/')
    backImg = models.ImageField(upload_to='moneyPhotos/back/')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

