from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-

from django.utils import timezone


class AccessToken(models.Model):
    token = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return self.token
    
class Dialer(models.Model):
    phone_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    # Id_no = models.CharField(max_length=10)

    def __str__(self):
        return self.phone_number

class AccessToken(models.Model):
    token = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return self.token

class Payment1(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('c2b', 'Customer to Business'),
        ('b2c', 'Business to Customer'),
        ('b2b', 'Business to Business'),
    ]

    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return self.phone_number
