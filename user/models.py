from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
# Customized user model e.g. for register and login by e-mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, first_name, last_name, phone_number=None, city=None, image=None, password=None,
                    is_staff=False, is_admin=False):
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
        user_obj.phone_number = phone_number
        user_obj.city = city
        if image is not None:
            user_obj.image = image
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, nickname, first_name, last_name, phone_number=None, city=None, image=None, email=None,
                         password=None):
        user = self.create_user(
            email,
            nickname=nickname,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            city=city,
            image=image,
            password=password,
            is_admin=True,
            is_staff=True,
        )
        return user


def upload_location(instance, filename):
    return "user ID %s/%s" %(instance.id, filename)


def default_place_pics():
    return "default.png"


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    phone_number = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(default='default.png', upload_to=upload_location, blank=True)

    def get_image(self):
        if not self.image:
            return settings.HOSTNAME + default_place_pics
        return settings.HOSTNAME + self.image

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'first_name', 'last_name']

    objects = UserManager()

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

    @property
    def is_staff(self):
        return self.staff

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)