from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class comments(models.Model):
    name = models.CharField(max_length=100, null=True)
    comment = models.TextField(null=True,blank=True,default='None')
    File = models.FileField(upload_to='', max_length=100,null=True)
    done_by = models.ForeignKey(User,  on_delete=models.CASCADE ,null=True,blank=True)
    created = models.DateTimeField( auto_now=True, auto_now_add=False ,null=True)
    updated = models.DateTimeField(null=True,auto_now=False,auto_now_add=True)
    

    def __str__(self):
        return f'Comment Written by { str(self.done_by)}'

    class meta:
        ordering = ('-created',)

    @property
    def FileUrl(self):
        try:
            url = self.File.url
        except:
                url = ''
                
        return url