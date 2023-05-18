from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager
)
from datetime import datetime





Bus_Type = (    
    ("Ac-seating", "Ac-seating"),
    ("Non-Ac-seating", "Non-Ac-seating"),
    ("Ac-sleeping", "Ac-slepping"),
    ("Non-Ac-sleeping", "Non-Ac-slepping")
)
Bus_category = (
  ("Local", "Local"),
    ("Express", "Express"),
)



class UserManager(BaseUserManager):
    def create_user(self, email,  username, password=None,**extra_fields):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('acivation_status', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError((
                'Super user must have is_staff'
            ))

        return self.create_user(email,username,password,**extra_fields)


class User(AbstractUser):
   

    profile_img=models.ImageField('image',null=True,blank=True,upload_to='profile',validators=[FileExtensionValidator(['png','jpg'])])
    acivation_status=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email




class Bus(models.Model):
    bus_name=models.CharField(max_length=500)
    bus_number=models.CharField(max_length=15)
    bus_category=models.CharField(max_length=20,choices=Bus_category)
    bus_type=models.CharField(max_length=20,choices=Bus_Type)
    bus_seat=models.CharField(max_length=10,null=True)
    bus_status=models.BooleanField(default=True)


    def __str__(self) :
        return self.bus_name

class JourneyRoot(models.Model):
    start_point=models.CharField(max_length=100000)
    end_point=models.CharField(max_length=1000000)
    kilometer=models.CharField(max_length=10) 
    one_kilometer_price=models.CharField(max_length=10,null=True,blank=True)
    price=models.CharField(max_length=10,null=True,blank=True)
    departure_date=models.DateField(null=True,blank=True)
    departure_time=models.TimeField(null=True,blank=True)
    arrival_date=models.DateField(null=True,blank=True)
    arrival_time=models.TimeField(null=True,blank=True)
    duration=models.CharField(max_length=100,null=True,blank=True)
    via=models.CharField(max_length=1000,null=True,blank=True)
    bus=models.ManyToManyField(Bus,symmetrical=False, related_name='buses')

    def Buses(self):
        return ",".join([str(b) for b in self.bus.all()])    
    
class BookTicket(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE,blank=True,null=True)
    journey=models.CharField(max_length=100,null=True,blank=True)
    seats=models.CharField(max_length=10,null=True,blank=True)
    slected_seat=models.CharField(max_length=100,null=True,blank=True)
    slected_seat=models.CharField(max_length=100,null=True,blank=True)
    fare=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=15,null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)
    book_date_time=models.DateTimeField(auto_now_add=True)
    departure_time=models.CharField(max_length=100,null=True,blank=True)
    arrival_time=models.CharField(max_length=100,null=True,blank=True)
    duration=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.user.username
    

class CancleTicket(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    cancle_bus=models.ForeignKey(BookTicket, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.user.username
    

