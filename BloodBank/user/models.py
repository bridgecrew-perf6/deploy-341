from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100,null=False)
    email = models.CharField(max_length=100,unique=True,null=False)
    password = models.CharField(max_length=20,null=False)
    bloodgroup = models.CharField(max_length=10,null=False)
    profilepic = models.CharField(max_length=200,null=False,default="/user/logo.png")
    otp = models.IntegerField(null=True)
    isverify = models.BooleanField(default=False)

    def __str__(self):
        return self.username + " : " + self.email

class BloodRequest(models.Model):        
    name = models.CharField(max_length=100,null=False)
    phone = models.CharField(max_length=20,null=False)
    hospital = models.CharField(max_length=100,null=False)
    city = models.CharField(max_length=100,null=False)
    bloodgroup = models.CharField(max_length=10,null=False)    
    requestby = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " : " + self.bloodgroup        
