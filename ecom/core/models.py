from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, 
                    email, 
                    fullname, 
                    phonenumber=None, 
                    role='customer',
                    password=None,
                    address=None,
                    
                    ):
        if not email:
            raise ValueError("Users must have an email address")
        if not fullname:
            raise ValueError("Users must provide a full name")

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
            phonenumber=phonenumber,
            role=role,
            address=address
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, phonenumber,role = 'admin' ,password=None,address=None):
        user = self.create_user(
            email=email,
            fullname=fullname,
            phonenumber=phonenumber,
            password=password,
            role=role,
            address=address
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):

    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(verbose_name="Email Address", max_length=255, unique=True)
    fullname = models.CharField(verbose_name="Full Name", max_length=150)
    phonenumber = models.CharField(verbose_name="Phone Number", max_length=20, blank=True, null=True)
    address = models.CharField(verbose_name="Address", max_length=255, blank=True, null=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer', verbose_name="User Role")
    
    # Required fields for Django's auth system
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # Link the custom manager
    objects = MyUserManager()

    # Log in using email instead of username
    USERNAME_FIELD = "email"
    
    # Fields prompted when running 'createsuperuser' (email and password are automatically required)
    REQUIRED_FIELDS = ["fullname","phonenumber","address"]

    def __str__(self):
        return self.email

    # Required permissions helper methods for Django Admin
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin