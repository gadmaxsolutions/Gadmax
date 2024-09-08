from django.db import models

from account.models import Account


# Create your models here.
class Contact(models.Model):

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True,blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=500, blank=True)
    reply_message = models.TextField(max_length=500, blank=True)
    reply_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RepliedContact(models.Model):

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=500, blank=True)
    reply_message = models.TextField(max_length=500, blank=True)  # New field for storing the reply
    replied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Replied to {self.name} on {self.replied_at}"