from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100,null=False)
    email = models.CharField(max_length=100,null=False)
    subject = models.CharField(max_length=200,null=False)
    message = models.CharField(max_length=2000,null=False)

    def __str__(self):
        return self.name + " : " + self.message