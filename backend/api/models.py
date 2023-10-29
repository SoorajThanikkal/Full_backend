from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager

class User(AbstractUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50)
    is_client = models.BooleanField(default=False)
    is_freelancer = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # Ensure either is_freelancer or is_client is set, but not both
        if self.is_freelancer and self.is_client:
            raise ValueError("A user cannot be both a freelancer and a client.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.email

    # Rest of your User model fields and methods...

class Client(models.Model):
    user = models.OneToOneField(User, related_name="client", on_delete=models.CASCADE)
    profilepic = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    last_name = models.CharField(max_length=50, default='')
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be a 10-digit number."
    )
    phone = models.CharField(max_length=10, validators=[phone_regex], blank=True, null=True)
    address = models.CharField(max_length=50, default='')
    about = models.TextField()
    
    def __str__(self):
        return self.user.username
    

    # Rest of your Client model fields...

  # Rest of your JobNames model fields...
class JobNames(models.Model):
    jobcategory = models.CharField(max_length=50, default='')

class Freelancer(models.Model):
    user = models.OneToOneField(User, related_name="freelancer", on_delete=models.CASCADE)
    profilepic = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    last_name = models.CharField(max_length=200, default='')
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be a 10-digit number."
    )
    phone = models.CharField(max_length=10, validators=[phone_regex], blank=True, null=True)
    job = models.ForeignKey(JobNames, on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=250, default='')
    rating = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    EXPERIENCE_CHOICES = (
    ('Entry Level', 'Entry Level'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
   )

    experiance = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='Entry Level')
    age = models.PositiveIntegerField(default=0)
    about = models.TextField(default='')
    price = models.PositiveIntegerField(default=0)
    portfolio = models.URLField(max_length=200, blank=True, null=True)
    availability = models.BooleanField(default=True)
    
    # Rest of your Freelancer model fields...



  
