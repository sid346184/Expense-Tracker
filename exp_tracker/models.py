from django.db import models
from datetime import datetime


# Create your models here.

class Accounts(models.Model):
    name=models.CharField(max_length=100)
    expense=models.FloatField(default=0.0)
    user=models.ForeignKey('auth.User', on_delete=models.CASCADE) # what it does is it creates a foreign key relationship with the User model provided by Django's auth system.
    liability_list =models.ManyToManyField('Expense',blank=True)

class Expense(models.Model):
    name=models.CharField(max_length=100)
    amount=models.FloatField(default=0.0)
    date=models.DateField(default=datetime.now,null=False)
    long_term=models.BooleanField(default=False)
    interest_rate=models.FloatField(default=0.0,null=True,blank=True)
    end_date=models.DateField(null=True,blank=True)
    monthly_expenses=models.FloatField(default=0.0,null=True,blank=True)
    user=models.ForeignKey('auth.User', on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if self.long_term:
            self.monthly_expenses = self.calculate_monthly_expenses()
        super(Expense, self).save(*args, **kwargs)

    def calculate_monthly_expenses(self):
        if self.long_term and self.end_date and self.date:
            # Calculate number of days between dates
            days = (self.end_date - self.date).days
            if days <= 0:
                return self.amount  # Return full amount if end_date is same or before start date
                
            if self.interest_rate == 0:
                # For zero interest, simply divide the amount by number of months
                months = max(1, days / 30)  # Ensure at least 1 month
                return self.amount / months
            else:
                # Calculate number of months between dates
                months = (self.end_date.year - self.date.year) * 12 + self.end_date.month - self.date.month
                if months <= 0:
                    return self.amount  # Return full amount if less than a month
                    
                # Calculate EMI using compound interest formula
                monthly_rate = self.interest_rate/12/100
                try:
                    monthly_expense = (self.amount * monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
                    return monthly_expense
                except (ZeroDivisionError, OverflowError):
                    return self.amount  # Return full amount if calculation fails
        return self.amount