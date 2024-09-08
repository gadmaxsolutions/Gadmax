from django.db import models

from account.models import Account


# Create your models here.
class SearchLog(models.Model):
    # user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    search_term = models.CharField(max_length=100)
    search_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        # return f'{self.user.username} - {self.search_term}'
        return f'{self.search_term}'


class FrequentSearch(models.Model):
    # user = models.ForeignKey(Account, on_delete=models.CASCADE)
    search_term = models.CharField(max_length=100)

    def __str__(self):
        # return f'{self.user.username} - {self.search_term}'
        return f'{self.search_term}'