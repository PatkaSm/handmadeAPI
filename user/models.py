from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
# Customized user model e.g. for register and login by e-mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, first_name, last_name, password=None, is_admin=False):
        if not email:
            raise ValueError("Musisz podać swój e-mail!")
        if not nickname:
            raise ValueError("Musisz podać swój nick!")
        if not password:
            raise ValueError("Musisz podać swoje hasło!")
        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.nickname = nickname
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, nickname, first_name, last_name, email, password=None):
        user = self.create_user(
            email,
            nickname=nickname,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_admin=True,
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'  # assigning an email as a username
    REQUIRED_FIELDS = ['nickname', 'first_name', 'last_name']  # set as necessary for filling

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_perm(perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class Profile(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.IntegerField(null=True)
    city = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    house_number = models.CharField(max_length=20, null=True)
    postOffice_number = models.CharField(max_length=6, null=True)
    image = models.ImageField(upload_to=)