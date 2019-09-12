from django.db import models

class user(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.IntegerField()
    dob = models.DateField()
    password = models.CharField(max_length=20)
    image = models.ImageField(upload_to='profile_image', default="default.jpg", blank=True, null=True)

    def __str__(self):
        return self.username

class friendlist(models.Model):
    userid = models.ForeignKey(user, on_delete=models.CASCADE, blank=True, null=True)
    friends = models.TextField(max_length=100, default=None, blank=True, null=True)

    def __str__(self):
        return self.userid.username

class post(models.Model):
    userid = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True)
    posts = models.ImageField(upload_to='posts', default=None, null=True, blank=True)

    def __str__(self):
        return self.userid.username

class notifications(models.Model):
    userid = models.ForeignKey(user, on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(max_length=20)
    friendrequest = models.CharField(max_length=20, null=True, blank=True)
    info = models.CharField(max_length=20, null=True, blank=True)