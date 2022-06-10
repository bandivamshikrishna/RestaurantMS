from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chef(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number=models.PositiveIntegerField()
    profile_pic=models.ImageField(upload_to='chef/profile_pic/',null=True)
    resume=models.FileField(upload_to='chef/resumes/',null=True)
    position=models.CharField(max_length=1000,null=True)
    approved=models.BooleanField(default=False)
