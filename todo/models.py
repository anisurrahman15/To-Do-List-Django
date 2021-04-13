from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    # blank = True will let the user update 'Datecompleted'
    # time or not update date complete time.

    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Last_Modified = models.DateTimeField(auto_now=True) # Update the Modification date.
    # auto_now will add the time when this model is modified.

    def __str__(self):
        return self.title
