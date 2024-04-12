from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
TYPE = (
    ('Positive', 'Credit'),
    ('Negative', 'Debit')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    income = models.FloatField(null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['user']
    
    def __str__(self):
            return f' User: {self.user} || Balance: {self.balance}'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    title = models.CharField(max_length = 100)
    amount = models.FloatField()
    expense_type = models.CharField(max_length=10, choices=TYPE, default='Positive')
    date = models.DateTimeField(default = timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        if self.expense_type == 'Positive':
            report = 'Credit'
        else:
            report = 'Debit'
        return f' {report}: {self.user} (N{self.amount})'


