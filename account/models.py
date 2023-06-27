from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True)
    phone_number = PhoneNumberField()
    responses = models.IntegerField(default=5)
    is_subscribed = models.BooleanField(default=False)
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE, null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.subscription is not None:
            self.responses = self.responses + self.subscription.responses
            self.is_subscribed = True
        if not self.username:
            self.username = self.email
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError("Email already exists")


    def __str__(self):
        return self.username


class Subscription(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    discount = models.IntegerField(help_text="Enter discount in percentage")
    discounted_price = property(lambda self: (self.price - (self.price * self.discount / 100)) - 1)
    responses = models.IntegerField(default=0)
    verified_tag = models.BooleanField(default=False)
    higher_position_in_search = models.BooleanField(default=False)
    property_description_by_expert = models.BooleanField(default=False)
    property_promotion = models.IntegerField(default=0)
    relationship_manager = models.BooleanField(default=False)
    professional_photoshoot = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Response(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    property = models.ForeignKey('property.Property', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


