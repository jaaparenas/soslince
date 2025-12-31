from django.db import models
from django.contrib.auth import get_user_model

class Staff(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __str__(self):
        return "%s" % self.user.first_name + " " + self.user.last_name


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class Customer(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='customer')
    phone = models.CharField(max_length=255, blank=True, null=True, unique=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    blood_type = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    secret_word = models.CharField(max_length=255, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.user.first_name + " " + self.user.last_name


class CustomerLocation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "%s" % str(self.timestamp) + " | " + self.customer.user.first_name + " " + self.customer.user.last_name


class CustomerSOS(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    status =  models.SmallIntegerField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s" % self.customer.user.first_name + " " + self.customer.user.last_name


class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    NIT = models.CharField(max_length=255, blank=True, null=True, unique=True) # Assuming NIT is a string
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name