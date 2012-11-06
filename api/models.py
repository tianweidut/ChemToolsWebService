from django.db import models

# Create your models here.

from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=50)
    complete = models.BooleanField(default=False, null=False)
    
    def __unicode__(self):
        return self.name